import logging
from pathlib import Path
import random
from .dataclasses import RatioSplit, SplitData
from ....common.enums import DatasetSplit
from ....common.io import FileWriter, FileReader
from ....common.utils import timestamp
from ....config.constants import RAW_TESTING_DIR, RAW_TRAINING_DIR, RAW_VALIDATION_DIR


logger = logging.getLogger(__name__)


class SplitDataService:

    def __init__(
            self, 
            input_path: Path, 
            ratios: dict[str, float],
            file_writer: FileWriter = FileWriter(),
            file_reader: FileReader = FileReader()
    ):
        self.input_path = input_path
        self.ratios = self._build_ratio_split(ratios)
        self._validate_ratios()
        self.file_writer = file_writer
        self.file_reader = file_reader
        self.input_data = self._input_data()
        self.file_paths: dict[DatasetSplit, Path] = {}

    def split_and_save_data(self):
        data = self._split_data_by_ratios()

        training_outfile = self._outfile_path(DatasetSplit.TRAINING)
        self._save_data(data.training, training_outfile)
        logger.debug(f"Successfully saved TRAINING data ({len(data.training)}) records) to {training_outfile}")

        validation_outfile = self._outfile_path(DatasetSplit.VALIDATION)
        self._save_data(data.validation, validation_outfile)
        logger.debug(f"Successfully saved VALIDATION data ({len(data.validation)}) records to {validation_outfile}")

        testing_outfile = self._outfile_path(DatasetSplit.TESTING)
        self._save_data(data.testing, testing_outfile)
        logger.debug(f"Successfully saved TESTING data ({len(data.training)}) records to {testing_outfile}")

    def _build_ratio_split(self, ratios: dict[str, float]) -> RatioSplit:
        ratio_split = RatioSplit(
            training=ratios["train_ratio"],
            validation=ratios["val_ratio"],
            testing=ratios["test_ratio"],
        )
        return ratio_split

    def _validate_ratios(self):
        total = self.ratios.training + self.ratios.validation + self.ratios.testing
        if abs(total - 1.0) > 0.001:
            msg = f"Invalid split ratios. train={self.ratios.training} val={self.ratios.validation} test={self.ratios.testing}... Should sum to 1.0!"
            logger.error(msg)
            raise RuntimeError(msg)
        logger.debug(f"Data ratios valid: train={self.ratios.training} val={self.ratios.validation} test={self.ratios.testing}")

    def _save_data(self, data: list[str], output_path: Path):
        text = "\n".join(data)
        self.file_writer.save(
            output_path=output_path, 
            text=text,
        )

    def _input_data(self, shuffle: bool = True) -> list[str]:
        data = self.file_reader.read_text_lines(file_path=self.input_path)
        if shuffle:
            random.shuffle(data)
        return data

    def _split_data_by_ratios(self) -> SplitData:
        total_lines = len(self.input_data)
        train_count = int(total_lines * self.ratios.training)
        val_count = int(total_lines * self.ratios.validation)
        return SplitData(
            training=self.input_data[:train_count],
            validation=self.input_data[train_count : train_count + val_count],
            testing=self.input_data[train_count + val_count:]
        )

    def _outfile_path(self, data_type: DatasetSplit) -> Path:
        output_dir = self._output_dir(data_type)
        file_name = f"{data_type.value}__{timestamp(intraday=True)}.txt"
        full_path = output_dir / file_name
        self.file_paths[data_type] = full_path
        return full_path
    
    def _output_dir(self, data_type: DatasetSplit) -> Path:
        match data_type:
            case DatasetSplit.TRAINING:
                directory = RAW_TRAINING_DIR
            case DatasetSplit.VALIDATION:
                directory = RAW_VALIDATION_DIR
            case DatasetSplit.TESTING:
                directory = RAW_TESTING_DIR
        return directory