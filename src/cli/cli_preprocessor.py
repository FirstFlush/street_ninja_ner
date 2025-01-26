import logging
from pathlib import Path
from src.common.enums import ModelType, DataType
from src.config import DATA_DIR
from src.preprocess import SpacyPreprocessor, PreprocessorConfig


logger = logging.getLogger(__name__)


class CLIPreprocessor:

    def __init__(self, config:PreprocessorConfig):

        self.config = config
        match config.model_type:
            case ModelType.SPACY:
                self.preprocessor = SpacyPreprocessor(config=config)
            case _:
                msg = f"{self.__class__.__name__}.__init__() Received invalid ModelType: `{self.config.model_type}`"
                logger.error(msg)
                raise ValueError(msg)

    @staticmethod
    def build_prepocessor_config(model:str, dataset_type:str) -> "PreprocessorConfig":
        try:
            model_type = ModelType(model)
            data_type = DataType(dataset_type)
        except ValueError:
            msg = f"One or more invalid command-line arguments for model_type: `{model_type}`, data_type: `{data_type}`"
            logger.error(msg)
            raise
        
        return PreprocessorConfig(
            model_type=model_type,
            data_type=data_type,
            DATA_DIR=DATA_DIR
        )

    def preprocess(self):
        """
        Trigger preprocessing based on the provided configuration.
        Combines all raw files from the specified raw directory and processes them.
        """
        logger.info("Starting preprocessing...")
        try:
            self.preprocessor.parse_raw_files()
        except Exception as e:
            logger.error(f"Spacy Preprocessing failed: {e}", exc_info=True)
            raise
        except:
            logger.info("Preprocessing completed successfully.")


    def list_raw_files(self):
        """
        List all raw files available in the configured raw directory.
        """
        raw_dir = self.preprocessor.raw_dir
        raw_files = list(raw_dir.glob("*.json"))
        if not raw_files:
            logger.warning(f"No raw files found in {raw_dir}")
            return []
        
        logger.info(f"Found {len(raw_files)} raw files in {raw_dir}")
        return [str(file) for file in raw_files]

    # def clean_processed(self):
    #     """
    #     Clean processed files from the relevant directory (training/validation).
    #     """
    #     processed_dir = DATA_DIR / "processed" / self.config.data_type.value
    #     logger.info(f"Cleaning processed files in {processed_dir}...")
    #     for ext_dir in ["json", "spacy"]:
    #         path = processed_dir / ext_dir
    #         if path.exists():
    #             for file in path.glob("*"):
    #                 file.unlink()
    #                 logger.info(f"Deleted: {file}")
    #     logger.info(f"Finished cleaning processed files in {processed_dir}.")



























    # def run(self):
    #     """
    #     Entry point for the CLI to call the preprocessing logic.
    #     Validates inputs and delegates the work to the SpacyPreprocessor.
    #     """
    #     try:
    #         print(f"Initializing SpacyPreprocessor with config: {self.config}")
    #         self.preprocessor = SpacyPreprocessor(self.config)

    #         print(f"Starting preprocessing for {self.config.data_type.value} data...")
    #         self.preprocessor.preprocess_all_raw_data()
    #         print("Preprocessing completed successfully.")

    #     except FileNotFoundError as e:
    #         logger.error(f"File not found: {e}", exc_info=True)
    #         print(f"Error: {e}")
    #     except Exception as e:
    #         logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    #         print(f"An unexpected error occurred: {e}")









    # def find_latest_file(self, directory: Path, extension: str) -> Path:
    #     files = list(directory.glob(f"*.{extension}"))
    #     if not files:
    #         msg = f"No files with extension {extension} found in {directory}"
    #         logger.error(msg, exc_info=True)
    #         raise FileNotFoundError(msg)
    #     return max(files, key=lambda f: f.stat().st_mtime)

    # # def preprocess(self, input_file: str, dataset_type: str, model: str):
    # #     """
    # #     Preprocess raw data into format required by the chosen model.
    # #     """
    # #     output_subdir = self.data_dir / "processed" / dataset_type
    # #     output_subdir.mkdir(parents=True, exist_ok=True)
    # #     preprocessor_config = PreprocessorConfig(
    # #         model_type=self.handler.model_type,
    # #         data_type=self.data_type,
    # #         DATA_DIR=DATA_DIR,
    # #     )
    # #     preprocessor = SpacyPreprocessor(config=preprocessor_config)
    # #     preprocessor.preprocess_label_studio_data(dataset_type=dataset_type, model=model)
