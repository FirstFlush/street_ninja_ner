from src.common.io import FileReader, FileWriter
from ..commands.docbin import DocbinCommand
from .base import BaseCliService
from pathlib import Path


class DocbinService(BaseCliService[DocbinCommand]):

    command_cls = DocbinCommand

    @classmethod
    def run(cls, **kwargs):
        service = cls()
        input_path = kwargs[service.command_cls.Kwargs.INPUT_PATH.value]
        command = service.build_command()
        service.execute_command(command, input_path)

    def build_command(self) -> DocbinCommand:
        file_writer = FileWriter(self.command_cls.OUTPUT_DIR)
        file_reader = FileReader()
        return DocbinCommand(file_writer=file_writer, file_reader=file_reader)

    def execute_command(self, command: DocbinCommand, input_path: Path):
        command.build_docbin(input_path)

