import logging
from pathlib import Path
from typing import Any
from .docbin import DocbinBuilder
from .label_studio_converter import LabelStudioConverter
from ....common.enums import DatasetSplit
from ....common.io import FileReader, FileWriter

logger = logging.getLogger(__name__)


class LabelStudioToDocbinService:

    def __init__(
            self,  
            split_enum: DatasetSplit,
            input_path: Path | None = None,
            input_data: Any | None = None,
            file_reader: FileReader = FileReader(),
            file_writer: FileWriter = FileWriter(),
    ):
        if not bool(input_path) ^ bool(input_data):
            msg = f"{self.__class__.__name__} requires exactly one of input_path or input_data, not both or neither."
            logger.error(msg)
            raise RuntimeError(msg)
        self.input_data = input_data
        self.input_path = input_path
        self.split_enum = split_enum
        self.file_reader = file_reader
        self.file_writer = file_writer
        self.labelstudio_converter, self.docbin_builder = self._build_services()

    def convert(self):
        if self.input_path is not None:
            json_path = self.labelstudio_converter.convert_from_file(self.input_path)
        elif self.input_data is not None:
            json_path = self.labelstudio_converter.convert_from_data(self.input_data, self.split_enum)
        else:
            msg = f"{self.__class__.__name__} neither input_path nor input_data is set! How??"
            logger.error(msg)
            raise RuntimeError(msg)
        
        self.docbin_builder.build_docbin(json_path, self.split_enum)


    def _build_services(self) -> tuple[LabelStudioConverter, DocbinBuilder]:
        labelstudio_converter = LabelStudioConverter(
            file_writer=self.file_writer,
            file_reader=self.file_reader,
        )
        logger.debug("Created LabelStudioConverter object")
        docbin_builder = DocbinBuilder(
            file_writer=self.file_writer,
            file_reader=self.file_reader,
        )
        logger.debug("Created DocbinBuilder object")
        return labelstudio_converter, docbin_builder