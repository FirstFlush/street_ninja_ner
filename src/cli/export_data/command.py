import logging
import os
import time
from typing import Any
from ..base_command import BaseCommand
from ...common.enums import DatasetSplit
from ...common.mappings import SPLIT_TO_LABELSTUDIO_NAME
from ...common.io import FileWriter
from ...common.api import ApiClient


logger = logging.getLogger(__name__)


class ExportUrls:

    PROJECTS_URL = f"http://localhost:8080/api/projects"

    def _base_project_url(self, split: DatasetSplit) -> str:
        return f"{self.PROJECTS_URL}/{SPLIT_TO_LABELSTUDIO_NAME[split]}"

    def create_snapshot(self, split: DatasetSplit) -> str:
        return f"{self._base_project_url(split)}/exports"

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

    def _build_headers(self) -> dict[str, str]:
        token = os.getenv("LABELSTUDIO_API_TOKEN", "")
        return {"Authorization": f"Token {token}"}

    def _create_snapshot(self, split_enum: DatasetSplit) -> tuple[int, bool]:
        try:
            response = self.api_client.post(
                url=self.urls.create_snapshot(split_enum),
                headers=self._build_headers(),
                json={"export_type": "json"},
            )
        except self.api_client.ApiError as e:
            msg = f"Failed to create snapshot due to unexpected error: {e}"
            logger.error(msg, exc_info=True)
            raise
        else:
            data = response.json()
            snapshot_id = data["id"]
            completed = True if data["status"] == "completed" else False
            logger.debug(f"Successfully created snapshot")
            return snapshot_id, completed

    def _wait_for_snapshot(self, split: DatasetSplit, snapshot_id: int):
        snapshot_completed = False
        counter = 0
        counter_limit = 100
        while snapshot_completed is False and counter <= counter_limit:
            response = self.api_client.get(
                url=self.urls.get_snapshot_by_id(split=split, id=snapshot_id)
            )
            data = response.json()
            for result in data["converted_formats"]:
                if result["id"] == snapshot_id:
                    if result["status"] == "completed":
                        logger.debug(f"Snapshot `{snapshot_id}` created successfully. Waiting complete.")
                        snapshot_completed = True
                    else:
                        logger.debug(f"Snapshot `{snapshot_id}` current status: `{result["status"]}`. Waiting...")
            counter += 1
            time.sleep(2)
        if counter_limit >= 100:
            msg = f"Snapshot API counter limit exceeded. Snapshot id `{snapshot_id}` for split `{split.value}`"
            logger.error(msg)
            raise ConnectionError(msg)

    def _download_snapshot(self, split_enun: DatasetSplit, snapshot_id: int) -> list[dict[str, Any]]:
        response = self.api_client.get(
            url=self.urls.download_snapshot(split_enun, snapshot_id),
            headers=self._build_headers(),
            params={"exportFormat": "json"},
        )
        return response.json()

    def export_data(self, split_enum: DatasetSplit) -> list[dict[str, Any]]:
        snapshot_id, completed = self._create_snapshot(split_enum)
        if not completed:
            self._wait_for_snapshot(split=split_enum, snapshot_id=snapshot_id)
        data = self._download_snapshot(split_enum, snapshot_id)
        return data
        # try:
        #     response = self.api_client.get(
        #         url=url,
        #         headers=headers,
        #         params=params,
        #     )
        # except self.api_client.ApiError as e:
        #     logger.error(f"Failed to export from Label-Studio: {e}")
        # else:
        #     data = response.json()
        #     logger.debug(f"Successfully exported {len(data)} inquiries")
        #     return data