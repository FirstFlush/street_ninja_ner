import logging

from ..base_service import BaseCliService
from .command import ExportDataCommand
from ...common.enums import DatasetSplit

logger = logging.getLogger(__name__)

class ExportDataService(BaseCliService):

    command_cls = ExportDataCommand

    @classmethod
    def run(cls):
        service = cls()
        


    def build_command(self, *args, **kwargs) -> ExportDataCommand:
        return self.command_cls()