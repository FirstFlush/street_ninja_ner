from pathlib import Path
import spacy
from typing import Any, cast
from spacy.tokens import DocBin
import logging
from ..common.enums import AnnotationLabels
from ..common.io import FileManager
from ..common.types import SpacyFormattedJson


logger = logging.getLogger(__name__)


class DocBinBuilder:
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

    def build_docbin(self, input_path: Path):
        json_data = self._get_json_data(input_path)
        output_path = self.file_manager.output_path(input_path, "spacy")
        self._convert_json_to_spacy(json_data, output_path)
        logger.info(f"Saved {len(json_data)} records to {output_path}")


    def _get_json_data(self, input_path: Path) -> list[SpacyFormattedJson]:
        json_data = self.file_manager.json_from_file(input_path)
        return self._validate_spacy_json(json_data)

    def _validate_spacy_json(self, data: Any) -> list[SpacyFormattedJson]:
        if not isinstance(data, list):
            raise ValueError("Expected a list of training examples")
        
        for entry in data:
            if not isinstance(entry, dict):
                raise ValueError("Each item must be a dict")
            if "text" not in entry or "entities" not in entry:
                raise ValueError("Missing required keys in training example")
            if not isinstance(entry["entities"], list):
                raise ValueError("'entities' must be a list")
        
        return cast(list[SpacyFormattedJson], data)

    def _convert_json_to_spacy(self, json_data: list[SpacyFormattedJson], output_path: Path):
        nlp = spacy.blank("en")
        doc_bin = DocBin()

        for example in json_data:
            text = example["text"]
            entities = example["entities"]
            doc = nlp.make_doc(text)
            spans = []
            for start, end, label in entities:
                if label not in AnnotationLabels.values():
                    continue
                span = doc.char_span(start, end, label=label)
                if span is None:
                    logger.debug(f"Skipping bad span: '{text[start:end]}'")
                    continue
                spans.append(span)
            doc.ents = spans
            doc_bin.add(doc)
        doc_bin.to_disk(output_path)

