import logging
import os
from typing import Any
from ..base_command import BaseCommand
from ...common.enums import DatasetSplit
from ...common.mappings import SPLIT_TO_LABELSTUDIO_NAME
from ...common.io import FileWriter
from ...common.api import ApiClient
# from ...config.constants import DATA_DIR

logger = logging.getLogger(__name__)


class ExportUrls:

    PROJECTS_URL = f"http://localhost:8080/api/projects"

    def _base_url(self, split: DatasetSplit):
        return f"{self.PROJECTS_URL}/{SPLIT_TO_LABELSTUDIO_NAME[split]}"

    def create_snapshot(self, split: DatasetSplit) -> str:
        return f"{self._base_url(split)}/exports"

    def get_snapshot_by_id(self, split: DatasetSplit, id: int) -> str:
        return f"{self.create_snapshot(split)}/{id}"

    def delete_snapshot(self, split: DatasetSplit, id: int) -> str:
        """Convenience method, same path as get_snapshot_by_id just send a DELETE method."""
        return self.get_snapshot_by_id(split, id)

    def download_snapshot(self, split: DatasetSplit, id: int) -> str:
        return f"{self.get_snapshot_by_id(split, id)}/download"


class ExportDataCommand(BaseCommand):

    urls = ExportUrls()    

    def __init__(
            self, 
            file_writer: FileWriter = FileWriter(),
            api_client: ApiClient = ApiClient(),
    ):
        self.file_writer = file_writer
        self.api_client = api_client


    def _export_data(self, url: str,) -> list[dict[str, Any]]:      # type: ignore
        token = os.getenv("LABELSTUDIO_API_TOKEN", "")
        headers = {"Authorization": f"Token {token}"}
        params = {"exportType": "JSON"}
        try:
            response = self.api_client.get(
                url=url,
                headers=headers,
                params=params,
            )
        except self.api_client.ApiError as e:
            logger.error(f"Failed to export from Label-Studio: {e}")
        else:
            data = response.json()
            logger.debug(f"Successfully exported {len(data)} inquiries")
            return data