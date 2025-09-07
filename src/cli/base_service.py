from abc import ABC, abstractmethod
import logging
from pathlib import Path
from typing import Type, TypeVar, Generic
from .base_command import BaseCommand

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseCommand)


class BaseCliService(Generic[T], ABC):
    
    command_cls: Type[T]

    def __init__(self):
        if self.command_cls is None:
            raise NotImplementedError(f"{self.__class__.__name__}.command_cls can not be None!")

    @abstractmethod
    def build_command(self, *args, **kwargs) -> BaseCommand:
        pass

    # @abstractmethod
    # def execute_command(self, command: BaseCommand, *args, **kwargs):
    #     pass

    @classmethod
    @abstractmethod
    def run(cls, *args, **kwargs):
        pass

    @staticmethod
    def _to_path(raw: str | Path, check: bool = False, create: bool = False) -> Path:
        """
        Converts a raw string to a Path object, with optional existence checks or directory creation.

        Raises:
            ValueError: If the input cannot be converted or check/create fails.
        """
        logger.debug(f"Attempting to convert raw input to Path: {raw}")
        try:
            path = Path(raw).expanduser().resolve()
            logger.debug(f"Resolved path: {path}")
        except Exception as e:
            logger.error(f"Failed to convert input to Path: {raw}")
            raise ValueError(f"Invalid path: {raw}") from e

        if check and not path.exists():
            logger.error(f"Path does not exist: {path}")
            raise ValueError(f"Path does not exist: {path}")

        if create:
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Created directory: {path}")
            except Exception as e:
                logger.error(f"Failed to create directory: {path}")
                raise ValueError(f"Failed to create directory: {path}") from e

        return path