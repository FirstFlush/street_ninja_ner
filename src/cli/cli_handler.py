import logging
from pathlib import Path
from src.config import DATA_DIR, OUTPUT_DIR
from src.common.enums import ModelType
from .cli_preprocessor import CLIPreprocessor
from .cli_training import CLITraining
import os


logger = logging.getLogger(__name__)


class CLIHandler:

    def __init__(self, model_type: ModelType):
        self.data_dir = DATA_DIR
        self.output_dir = OUTPUT_DIR
        self.model_type = model_type
        self._preprocessor = CLIPreprocessor
        self._training = CLITraining


    def build_preprocessor(self, model:str, dataset_type:str) -> CLIPreprocessor:
        config = CLIPreprocessor.build_prepocessor_config(model=model, dataset_type=dataset_type)
        return CLIPreprocessor(config)

    # def find_latest_file(self, directory: Path, extension: str) -> Path:
    #     files = list(directory.glob(f"*.{extension}"))
    #     if not files:
    #         msg = f"No files with extension {extension} found in {directory}"
    #         logger.error(msg, exc_info=True)
    #         raise FileNotFoundError(msg)
    #     return max(files, key=lambda f: f.stat().st_mtime)

    # def preprocess(self, input_file: str, dataset_type: str, model: str):
    #     """
    #     Preprocess raw data into format required by the chosen model.
    #     """
    #     output_subdir = self.data_dir / "processed" / dataset_type
    #     output_subdir.mkdir(parents=True, exist_ok=True)
    #     preprocessor_config = 
    #     preprocessor = SpacyPreprocessor(input_file=input_file, DATA_DIR=self.data_dir)
    #     preprocessor.preprocess_label_studio_data(dataset_type=dataset_type, model=model)




    def train(self, train_file: str = None, dev_file: str = None):
        train_file = train_file or self.find_latest_file(self.data_dir / "processed" / "training", ".spacy")
        dev_file = dev_file or self.find_latest_file(self.data_dir / "processed" / "validation", ".spacy")
        # click.echo(f"Training with:\n  Train file: {train_file}\n  Validation file: {dev_file}")

        command = f"python -m spacy train config.cfg --output {self.output_dir} --paths.train {train_file} --paths.dev {dev_file}"
        # click.echo(f"Running: {command}")
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        os.system(command)

