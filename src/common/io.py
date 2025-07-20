from collections.abc import Iterable
from datetime import datetime, timezone
import logging
from pathlib import Path
import json
from typing import Any


logger = logging.getLogger(__name__)


class FileManager:

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def output_path(self, input_path: Path, ext: str) -> Path:
        ext = ext.lstrip(".")
        return self.output_dir / f"{input_path.stem}__{self._timestamp()}.{ext}"

    def json_from_file(self, file_path: Path) -> Any:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug(f"Loaded JSON data from {file_path}")
        return data
    
    def json_from_files(self, dir_path: Path, **globbing_kwargs) -> Any:
        file_paths = dir_path.glob("*.json", **globbing_kwargs)
        data_aggregate = []
        for file_path in file_paths:
            data = self.json_from_file(file_path)
            if isinstance(data, Iterable):
                data_aggregate.extend(data)



    def save_json(self, output_path: Path, json_data: Any):
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(json_data, out, indent=2)

    def _timestamp(self) -> str:
        return datetime.now(tz=timezone.utc).strftime("%y-%m-%d_%H-%M-%S")
