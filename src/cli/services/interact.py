from .base import BaseCliService
from ..commands.interact import InteractCommand
import logging
from pathlib import Path
from typer import Exit

logger = logging.getLogger(__name__)

class InteractService(BaseCliService[InteractCommand]):

    command_cls = InteractCommand

    def _inquiry_length_valid(self, inquiry: str) -> bool:
        if 1 <= len(inquiry) <= 256:
            return True
        return False

    @classmethod
    def run(cls, **kwargs):
        service = cls()
        inquiry = kwargs[service.command_cls.Args.INQUIRY.value].strip()
        model_dir = kwargs.get(service.command_cls.Kwargs.MODEL_DIR.value)

        if not service._inquiry_length_valid(inquiry):
            logger.error(f"Inquiry length `{len(inquiry)}` invalid. Must be between 1 <= 256 chars.")
            Exit(code=1)

        command = service.build_command(model_dir)
        service.execute_command(command, inquiry)

    def build_command(self, model_dir: Path | None = None) -> InteractCommand:
        if model_dir:
            return InteractCommand(model_dir=model_dir)
        else:
            return InteractCommand()

    def execute_command(self, command: InteractCommand, inquiry: str):
        command.parse_and_print(inquiry)