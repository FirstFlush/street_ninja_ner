import logging
from pathlib import Path
from src.config import DATA_DIR, BASE_DIR, OUTPUT_DIR, Defaults
from src.common.enums import ModelType
from .cli_preprocessor import CLIPreprocessor
from .cli_training import CLITraining
import os


logger = logging.getLogger(__name__)


class CLIHandler:

    MODEL_CHOICES = ["spacy", "hugging_face"]
    DATASET_TYPE_CHOICES = ["training", "validation"]

    def __init__(self):
        self.data_dir = DATA_DIR
        self.output_dir = OUTPUT_DIR
        self._preprocessor = CLIPreprocessor
        self._training = CLITraining

    def _resolve_path(input_path: str) -> Path:
        """
        Resolves the given path. If it's relative, prepends BASE_DIR.
        If it's absolute, returns as-is.
        """
        path = Path(input_path)
        if not path.is_absolute():
            path = BASE_DIR / path
        return path.resolve()


    def build_preprocessor(self, model:str, dataset_type:str) -> CLIPreprocessor:
        config = self._preprocessor.build_prepocessor_config(model=model, dataset_type=dataset_type)
        return self._preprocessor(config)


    def build_training(
            self,
            model:str = Defaults.MODEL,
            config_path:str = Defaults.CONFIG_PATH,
            output_dir:str = Defaults.OUTPUT_DIR
    ) -> CLITraining:
        config = self._training.build_training_config(
            model=ModelType(model),
            config_path=self._resolve_path(config_path),
            output_dir=self._resolve_path(output_dir),
        )
        return self._training(config)


