from pathlib import Path
from .base import BaseCliService
from ..commands.label_studio_converter import LabelStudioCommand
from ...common.io import FileReader, FileWriter


class LabelStudioService(BaseCliService[LabelStudioCommand]):

    command_cls = LabelStudioCommand

    def build_command(self) -> LabelStudioCommand:
        output_dir = LabelStudioCommand.OUTPUT_DIR
        file_writer = FileWriter(output_dir)
        file_reader = FileReader()

        return LabelStudioCommand(
            file_writer=file_writer, 
            file_reader=file_reader
        )

    def execute_command(self, command: LabelStudioCommand, input_path: Path):
        command.convert(input_path)

    @classmethod
    def run(cls, **kwargs):
        service = cls()
        input_path = service._to_path(kwargs[cls.command_cls.Kwargs.INPUT_PATH.value])
        command = service.build_command()
        service.execute_command(
            command=command, 
            input_path=input_path
        )