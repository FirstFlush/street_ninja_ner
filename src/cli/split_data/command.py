import logging
from pathlib import Path
import random
from typing import Type
from ..base_command import BaseCommand
from .dataclasses import RatioSplit, SplitData
from ...common.enums import DatasetSplit
from ...common.io import ConsoleWriter, FileWriter, FileReader
from ...common.utils import timestamp
from ...config.constants import RAW_TESTING_DIR, RAW_TRAINING_DIR, RAW_VALIDATION_DIR


logger = logging.getLogger(__name__)


class SplitDataCommand(BaseCommand):

    def __init__(
            self, 
            input_path: Path, 
            ratios: RatioSplit,
            file_writer_cls: Type[FileWriter] = FileWriter,
            file_reader: FileReader = FileReader()
    ):
        self.input_path = input_path
        self.ratios = ratios
        self.file_writer_cls = file_writer_cls
        self.file_reader = file_reader
        self.input_data = self._input_data()

    def split_and_save_data(self):
        data = self._split_data_by_ratios()

        self._save_data(data.training, data_type=DatasetSplit.TRAINING)
        logger.debug("Successfully saved TRAINING data")

        self._save_data(data.validation, data_type=DatasetSplit.VALIDATION)
        logger.debug("Successfully saved VALIDATION data")

        self._save_data(data.testing, data_type=DatasetSplit.TESTING)
        logger.debug("Successfully saved TESTING data")

    def delete_input(self):
        self.input_path.unlink()
        logger.debug(f"Successfully deleted raw input file `{str(self.input_path)}`")


    def _save_data(self, data: list[str], data_type: DatasetSplit):

        output_dir = self._output_dir(data_type)
        file_name = f"{data_type.value}__{timestamp(intraday=True)}.txt"
        full_path = output_dir / file_name
        text = "\n".join(data)
        writer = self.file_writer_cls(output_dir)
        writer.save(
            output_path=full_path, 
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

    def _output_dir(self, data_type: DatasetSplit) -> Path:
        match data_type:
            case DatasetSplit.TRAINING:
                directory = RAW_TRAINING_DIR
            case DatasetSplit.VALIDATION:
                directory = RAW_VALIDATION_DIR
            case DatasetSplit.TESTING:
                directory = RAW_TESTING_DIR
        return directory