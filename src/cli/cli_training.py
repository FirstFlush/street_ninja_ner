import logging
from pathlib import Path
from common.enums import ModelType
from src.config import DATA_DIR, Defaults
from src.train import TrainingConfig, SpacyTraining


logger = logging.getLogger(__name__)


class CLITraining:
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        match self.config.model:
            case ModelType.SPACY:
                self.training = SpacyTraining(config)
            case _:
                msg = f"{self.__class__.__name__}.__init__() Received invalid ModelType: `{self.config.model}`"
                logger.error(msg)
                raise ValueError(msg)

    @staticmethod
    def _build_spacy_training_command(
            model:ModelType, 
            config_path:Path, 
            output_dir:Path, 
            train_file:Path, 
            dev_file:Path
    ) -> list[str]:
        """Builds the actual CLI command to train with SpaCy model"""
        return [
            "python", "-m", model, "train",
            str(config_path),
            "--output", str(output_dir),
            "--paths.train", str(train_file),
            "--paths.dev", str(dev_file),
        ]

    @classmethod
    def build_training_config(cls, model: ModelType, config_path: Path, output_dir: Path) -> TrainingConfig:
        match model:
            case ModelType.SPACY:
                train_file = DATA_DIR / "processed" / "training" / "spacy" / "training_data.spacy"
                dev_file = DATA_DIR / "processed" / "validation" / "spacy" / "validation_data.spacy"
                command = cls._build_spacy_training_command(
                    model=model,
                    config_path=config_path,
                    output_dir=output_dir,
                    train_file=train_file,
                    dev_file=dev_file,
                )
            case _:
                msg = f"Can not build TrainingConfig object. Invalid ModelType enum: `{model}`"
                logger.error(msg)
                raise ValueError(msg)
        logger.info(f"Training command: `{" ".join(command)}`")
        return TrainingConfig(
            train_file=train_file,
            dev_file=dev_file,
            model=model,
            config_path=config_path,
            output_dir=output_dir,
            command=command,
        )
    
    def train(self):
        if not hasattr(self, 'training'):
            msg = f"`{self.__class__.__name__}` has no attribute 'training'."
            logger.error(msg)
            raise AttributeError(msg)
        self.training.train()
        
    