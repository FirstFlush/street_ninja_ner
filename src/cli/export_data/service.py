import logging
from typing import Any
from ..base_service import BaseCliService
from .command import ExportDataCommand
from ...common.enums import DatasetSplit
from .labelstudio_to_docbin.service import LabelStudioToDocbinService

logger = logging.getLogger(__name__)

class ExportDataService(BaseCliService):

    command_cls = ExportDataCommand

    @classmethod
    def run(cls):
        export_service = cls()
        command = export_service.build_command()
        for split_enum in DatasetSplit:
            exported_data = command.export_data(DatasetSplit(split_enum))
            conversion_service = export_service.build_conversion_service(split_enum, exported_data)
            conversion_service.convert()
            logger.debug(f"Successfully exported data for split `{split_enum.value}`")
        logger.debug("Label-Studio export complete")

    def build_conversion_service(self, split_enum: DatasetSplit, json: list[dict[str, Any]]) -> LabelStudioToDocbinService:
        conversion_service = LabelStudioToDocbinService(
            input_data=json,
            split_enum=split_enum,
        )
        logger.debug(f"Successfully built {conversion_service.__class__.__name__}")
        return conversion_service

    def build_command(self) -> ExportDataCommand:
        return self.command_cls()