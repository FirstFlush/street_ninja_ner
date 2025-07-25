import logging
from pathlib import Path
from typing import Any, cast
from ....common.io import FileReader, FileWriter
from ....common.types import LabelStudioAnnotatedJson, SpacyFormattedJson
from ....common.enums import DatasetSplit
from ....config.constants import DATA_DIR


logger = logging.getLogger(__name__)


class LabelStudioConverter:

    OUTPUT_DIR = DATA_DIR / "converted"

    split_to_filename = {
        DatasetSplit.TESTING : "testing",
        DatasetSplit.TRAINING : "training",
        DatasetSplit.VALIDATION : "validation",
    }

    def __init__(self, file_writer: FileWriter, file_reader: FileReader = FileReader()):
        self.file_writer = file_writer
        self.file_reader = file_reader

    def convert(self, input_path: Path) -> Path:
        output_path = self.file_writer.output_path(input_path.stem, "json")
        json_data = self._get_json_data(input_path)
        converted_data = self._convert(json_data)
        self.file_writer.save_json(output_path=output_path, json_data=converted_data)
        logger.info(f"Saved {len(json_data)} records to {output_path}")
        
        return output_path

    def _get_json_data(self, input_path: Path) -> list[LabelStudioAnnotatedJson]:
        json_data = self.file_reader.json_from_file(input_path)
        return self._validate_labelstudio_json(json_data)

    def _validate_labelstudio_json(self, data: Any) -> list[LabelStudioAnnotatedJson]:
        if not isinstance(data, list):
            raise ValueError("Expected a list of label studio annotations")

        for i, entry in enumerate(data):
            if not isinstance(entry, dict):
                raise ValueError(f"Item at index {i} must be a dict")
            if "data" not in entry or "annotations" not in entry:
                raise ValueError(f"Item at index {i} missing 'data' or 'annotations' keys")
            if not isinstance(entry["data"], dict):
                raise ValueError(f"'data' in item {i} must be a dict")
            if "text" not in entry["data"]:
                raise ValueError(f"'data' in item {i} must contain 'text'")
            if not isinstance(entry["annotations"], list):
                raise ValueError(f"'annotations' in item {i} must be a list")

        return cast(list[LabelStudioAnnotatedJson], data)
    
    def _convert(self, json_data: list[LabelStudioAnnotatedJson]) -> list[SpacyFormattedJson]:
        """Convert Label Studio JSON to spaCy training format."""
        converted_data: list[SpacyFormattedJson] = []
        for item in json_data:
            text = item["data"]["text"]
            entities = []
            results = item.get("annotations", [])[0].get("result", [])
            for r in results:
                start = r["value"]["start"]
                end = r["value"]["end"]
                label = r["value"]["labels"][0]
                entities.append([start, end, label])
            converted_data.append({
                "text": text,
                "entities": entities
            })

        return converted_data
