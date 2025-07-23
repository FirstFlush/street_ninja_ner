from pathlib import Path
from .base import BaseCliService
from ..commands.labelstudio_to_docbin.command import LabelStudioToDocbinCommand
from ...common.enums import DatasetSplit

class LabelStudioToDocbinService(BaseCliService[LabelStudioToDocbinCommand]):

    command_cls = LabelStudioToDocbinCommand

    @classmethod
    def run(cls, **kwargs):
        service = cls()
        input_path = service._to_path(kwargs[service.command_cls.Kwargs.INPUT_PATH.value].strip())
        split = kwargs[service.command_cls.Kwargs.DATASET_SPLIT.value]
        command = service.build_command()
        service.execute_command(command, input_path, split)

    def build_command(self) -> LabelStudioToDocbinCommand:
        return LabelStudioToDocbinCommand()

    def execute_command(self, command: LabelStudioToDocbinCommand, input_path: Path, split: DatasetSplit):
        json_path = command.labelstudio_converter.convert(input_path)
        command.docbin_builder.build_docbin(json_path, split)