from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
import subprocess
from pathlib import Path
from common.enums import ModelType


logger = logging.getLogger(__name__)


@dataclass
class TrainingConfig:
    model: ModelType
    train_file: Path
    dev_file: Path
    config_path: Path
    output_dir: Path
    command: list[str]


class BaseTraining(ABC):

    def __init__(self, config:TrainingConfig):
        self.config = config

    @abstractmethod
    def train(self):
        ...


class SpacyTraining(BaseTraining): 
    
    def train(self):
        """
        Execute the `spacy train` command using the provided configuration.
        """
        try:
            subprocess.run(self.config.command, check=True)
        except subprocess.CalledProcessError as e:
            msg = f"Training failed wth error: {e}"
            logger.error(msg, exc_info=True)
            raise