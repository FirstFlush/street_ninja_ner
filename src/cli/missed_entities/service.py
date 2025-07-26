from pathlib import Path
from ..base_service import BaseCliService
from .command import MissedEntitiesCommand
from ...common.io import ConsoleWriter, FileReader

class MissEntitiesService(BaseCliService[MissedEntitiesCommand]):

    command_cls = MissedEntitiesCommand

    @classmethod
    def run(cls, **kwargs):
        service = cls()
        input_path = service._to_path(kwargs[service.command_cls.Kwargs.INPUT_PATH.value])
        command = service.build_command()
        service.execute_command(command, input_path)

    def build_command(self) -> MissedEntitiesCommand:
        return MissedEntitiesCommand(
            file_reader=FileReader(),
            console_writer=ConsoleWriter(),
        )

    def execute_command(self, command: MissedEntitiesCommand, input_path: Path):
        command.echo_missed_entities(json_path=input_path)
        return

