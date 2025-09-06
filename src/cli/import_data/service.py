import logging
from pathlib import Path
from ...common.enums import DatasetSplit
from .command import ImportCommand
from ..base_service import BaseCliService
from .split_data.service import SplitDataService

logger = logging.getLogger(__name__)


class ImportService(BaseCliService):

    command_cls = ImportCommand

    @classmethod
    def run(cls, input_path: Path, ratios: dict[str, float]):
        service = cls()

        split_data_service = SplitDataService(input_path=input_path, ratios=ratios)
        split_data_service.split_and_save_data()
        service._delete_input_path(input_path)

        command = service.build_command(split_data_service.file_paths)
        command.import_files()
        
    def build_command(self, files: dict[DatasetSplit, Path]) -> ImportCommand:
        return self.command_cls(files=files)

    def _delete_input_path(self, input_path: Path):
        input_path.unlink()
        logger.debug(f"Successfully deleted raw input file `{input_path}`")