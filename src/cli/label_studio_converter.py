import logging
from pathlib import Path
from typing import Any, cast
from ..common.io import FileManager
from ..common.types import LabelStudioAnnotatedJson, SpacyFormattedJson


logger = logging.getLogger(__name__)


class LabelStudioConverter:

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

    def convert(self, input_path: Path):
        output_path = self.file_manager.output_path(input_path, "json")
        json_data = self._get_json_data(input_path)
        converted_data = self._convert(json_data)
        self.file_manager.save_json(output_path=output_path, json_data=converted_data)
        logger.info(f"Saved {len(json_data)} records to {output_path}")

    def _get_json_data(self, input_path: Path) -> list[LabelStudioAnnotatedJson]:
        json_data = self.file_manager.json_from_file(input_path)
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
