import logging
from pathlib import Path
from typer import Exit
from typing import Type
from src.cli.base_command import BaseCommand
from ..base_service import BaseCliService
from .command import SplitDataCommand
from .dataclasses import RatioSplit

logger = logging.getLogger(__name__)


class SplitDataService(BaseCliService):

    command_cls: Type[SplitDataCommand] = SplitDataCommand

    def __init__(self, split: dict[str, float]):
        self.split = self._build_split(split)
        self._validate_split()

    def build_command(self, input_path: Path) -> SplitDataCommand:
        return self.command_cls(
            input_path=input_path,
            ratios=self.split,
        )

    @classmethod
    def run(cls, input_path: Path, split: dict[str, float]):
        service = cls(split)
        command = service.build_command(input_path)
        command.split_and_save_data()
        command.delete_input()

    def _build_split(self, split: dict[str, float]) -> RatioSplit:
        return RatioSplit(
            training=split["train_ratio"],
            validation=split["validation_ratio"],
            testing=split["testing_ratio"],
        )

    def _validate_split(self):
        total = self.split.training + self.split.validation + self.split.testing
        if abs(total - 1.0) > 0.001:
            msg = f"Invalid split ratio. train={self.split.training} val={self.split.validation} test={self.split.testing}... Should sum to 1.0!"
            logger.error(msg)
            Exit(code=1)