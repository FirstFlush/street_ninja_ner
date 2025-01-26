from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from spacy.tokens import DocBin
import spacy
from typing import Any, Literal
from .config import DATA_DIR
from .common.enums import ModelType, DataType, RawDataFormat


logger = logging.getLogger(__name__)

Entity = tuple[int, int, str]
Annotations = dict[Literal["entities"], list[Entity]]  # e.g. {"entities": [(5, 9, "RESOURCE"), ...]}
NormalizedData = list[tuple[str, Annotations]]

@dataclass
class PreprocessorConfig:
    model_type: ModelType
    data_type: DataType
    # raw_format: RawDataFormat
    DATA_DIR: Path = DATA_DIR


class BasePreprocessor(ABC):

    def __init__(self, config: PreprocessorConfig):

        self.config = config
        self.timestamp = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')
        match self.config.data_type:
            case DataType.TRAINING:
                self.raw_dir = DATA_DIR / "raw" / "training"
            case DataType.VALIDATION:
                self.raw_dir = DATA_DIR / "raw" / "validation"
            case _:
                msg = f"Invalid DataType enum value for PreprocessorConfig.data_type: `{config.data_type}`"
                logger.error(msg, exc_info=True)
                raise ValueError(msg)
        self.raw_files = self._get_raw_data_files()

    def _output_path(self, ext: str) -> Path:
        data_subdir = "training" if self.config.data_type == DataType.TRAINING else "validation"
        return DATA_DIR / "processed" / data_subdir / ext.lower() / f"spacy_{data_subdir}_data__{self.timestamp}.{ext}"

    def _get_raw_data_files(self) -> list[Path]:
        """
        Get all raw JSON files in the specified raw directory.
        """
        raw_files = list(self.raw_dir.glob("*.json"))
        if not raw_files:
            logger.warning(f"No raw JSON files found in `{self.raw_dir}`")
        else:
            logger.info(f"Found {len(raw_files)} raw JSON files. Processing...")
        return raw_files


    @staticmethod
    def _detect_raw_data_format(raw_data:Any) -> RawDataFormat:
        """
        Detect the format of a raw JSON file based on its structure.

        Args:
            file_path (Path): Path to the JSON file.

        Returns:
            str: The detected format ("label_studio" or "json_minimal").
        """
        if isinstance(raw_data, list):
            if all(isinstance(entry, list) and len(entry) == 2 for entry in raw_data):
                return RawDataFormat.JSON_MINIMAL
            elif all("annotations" in entry and "data" in entry for entry in raw_data):
                return RawDataFormat.LABEL_STUDIO
        raise ValueError("Unknown raw_data foramt")

    @abstractmethod
    def parse_raw_data(self, raw_data:Any, raw_format:RawDataFormat) -> NormalizedData:
        ...

    @abstractmethod
    def save_data(self, normalized_data: NormalizedData):
        ...


class SpacyPreprocessor(BasePreprocessor):
    """
    Prepare raw, annotated JSON data from label-studio and output it to
    ml/data/processed as both .json and .spacy formats.
    Combines all raw files in data/raw/ into a single processed file.
    """

    def __init__(self, config:PreprocessorConfig):
        super().__init__(config=config)
        self.output_json_path = self._output_path("json")
        self.output_spacy_path = self._output_path(config.model_type.value)

    def parse_raw_files(self):
        aggregated_data = []
        for raw_file in self.raw_files:
            logger.info(f"Processing file: {raw_file}")
            with open(raw_file, "r") as f:
                raw_data = json.load(f)
            try:
                raw_format = self._detect_raw_data_format(file_path=raw_file)
            except ValueError:
                msg = f"Unknown raw data format in file: `{raw_file}`"
                logger.error(msg, exc_info=True)
                raise

            try:
                raw_data = self.parse_raw_data(raw_file=raw_file, raw_format=raw_format)
                aggregated_data.extend(raw_data)
            except Exception as e:
                logger.error(f"Failed to parse file: `{raw_file}`, resulting in error: {e}", exc_info=True)
                raise

        self.save_data(aggregated_data)

    def parse_raw_data(self, raw_data: Any, raw_format:RawDataFormat) -> NormalizedData:
        """
        Route raw data parsing based on the raw data type.
        
        Args:
            raw_file (Path): Path to the raw JSON file.
        """
        match raw_format:
            case RawDataFormat.LABEL_STUDIO:
                return self.parse_label_studio_data(raw_data)
            case RawDataFormat.JSON_MINIMAL:
                return self.parse_json_minimal(raw_data)
            case _:
                raise ValueError(f"Unsupported raw data type: `{raw_format}`")

    def parse_json_minimal(self, raw_data:NormalizedData) -> NormalizedData:
        """
        Process already minimal, post-processed JSON data and prepare it for spaCy training.

        Args:
            raw_data (list): The post-processed JSON data in the minimal format.
                [
                    [
                        "need food 1166 melville st",
                        {
                            "entities": [
                                [5, 9, "RESOURCE"],
                                [10, 26, "ADDRESS"]
                            ]
                        }
                    ],
                    // etc...
                ]
        """
        return raw_data

    def save_data(self, normalized_data: NormalizedData):
        """
        Save normalized data to both JSON and spaCy formats.
        """
        # Prepare file paths
        # output_json_path = self.output_dir / "json" / f"{self.data_type.value}_data.json"
        # output_spacy_path = self.output_dir / "spacy" / f"{self.data_type.value}_data.spacy"

        # Save JSON
        with open(self.output_json_path, "w") as f:
            json.dump(normalized_data, f, indent=4)
        logger.info(f"Processed JSON data saved to {self.output_json_path}")

        # Save spaCy format
        nlp = spacy.blank("en")
        doc_bin = DocBin()

        for text, annotations in normalized_data:
            doc = nlp.make_doc(text)
            spans = []
            for start, end, label in annotations["entities"]:
                span = doc.char_span(start, end, label=label)
                if span:
                    spans.append(span)
                else:
                    logger.warning(f"Skipping invalid span: {text[start:end]} ({start}, {end})")
            doc.ents = spans
            doc_bin.add(doc)

        doc_bin.to_disk(self.output_spacy_path)
        logger.info(f"Processed spaCy data saved to {self.output_spacy_path}")


    def parse_label_studio_data(self, raw_data: list[dict[str, Any]]) -> NormalizedData:
        """
        Parse Label-Studio-style data into the normalized format.
        """
        parsed_data = []
        for item in raw_data:
            text = item["data"]["text"]
            entities = []

            for annotation in item["annotations"]:
                for result in annotation["result"]:
                    start = result["value"]["start"]
                    end = result["value"]["end"]
                    label = result["value"]["labels"][0]
                    entities.append((start, end, label))

            parsed_data.append((text, {"entities": entities}))
        return parsed_data
