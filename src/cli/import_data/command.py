import logging
import os
from pathlib import Path
from typing import Any
from ..base_command import BaseCommand
from ...common.api import ApiClient
from ...common.enums import DatasetSplit
from ...common.io import FileReader
from ...common.mappings import SPLIT_TO_LABELSTUDIO_NAME


logger = logging.getLogger(__name__)


class ImportCommand(BaseCommand):
    
    PROJECTS_URL = f"http://localhost:8080/api/projects"
    SPLIT_TO_LABELSTUDIO_NAME = SPLIT_TO_LABELSTUDIO_NAME

    def __init__(
            self, 
            files: dict[DatasetSplit, Path],
            file_reader: FileReader = FileReader(),
            api_client: ApiClient = ApiClient(),
    ):
        self.files = files
        self.file_reader = file_reader
        self.api_client = api_client

    def import_files(self):
        for split, path in self.files.items():
            project_name = self._project_name(split)
            label_studio_import_path = self._label_studio_import_url(project_name)
            data = self._txt_to_labelstudio_json(path)
            self._import_to_labelstudio(
                import_url=label_studio_import_path,
                tasks=data,
            )
            logger.debug(f"Successfully imported `{path}` to split `{split.value}`")

    def _import_to_labelstudio(self, import_url: str, tasks: list[dict[str, Any]]):
        token = os.getenv("LABELSTUDIO_API_TOKEN", "")
        if not token:
            msg = f"Missing label-studio API token. Did you forget to set an environment variable?"
            logger.error(msg)
            raise RuntimeError(msg)
        
        headers = {"Authorization": f"Token {token}"}
        response = self.api_client.post(
            url=import_url,
            json=tasks,
            headers=headers,
        )
        response.raise_for_status()

    def _label_studio_import_url(self, project_name: str) -> str:
        return f"{self.PROJECTS_URL}/{project_name}/import"

    def _project_name(self, split: DatasetSplit) -> str:
        return self.SPLIT_TO_LABELSTUDIO_NAME[split]

    def _txt_to_labelstudio_json(self, path: Path) -> list[dict[str, Any]]:
        """
        Convert .txt data to expected LabelStudio input format:
        [
            {"data": {"text": "need food at 222 main st"}},
            {"data": {"text": "where's shelter near hastings?"}},
        ]
        """
        data = self.file_reader.read_text(path)
        tasks = [{"data": {"text": line.strip()}} for line in data if line.strip()]
        return tasks