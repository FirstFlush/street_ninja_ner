import logging
from enum import Enum
from ...common.io import FileReader, FileWriter
from ..base_command import BaseCommand
from ._docbin import DocbinBuilder
from ._label_studio_converter import LabelStudioConverter

logger = logging.getLogger(__name__)

class LabelStudioToDocbinCommand(BaseCommand):

    def __init__(self):
        file_reader = FileReader()
        self.labelstudio_converter = LabelStudioConverter(
            file_writer=FileWriter(LabelStudioConverter.OUTPUT_DIR),
            file_reader=file_reader,
        )
        logger.debug("Created LabelStudioConverter object")
        self.docbin_builder = DocbinBuilder(
            file_writer=FileWriter(DocbinBuilder.OUTPUT_DIR),
            file_reader=file_reader,
        )
        logger.debug("Created DocbinBuilder object")

    class Kwargs(Enum):

        INPUT_PATH = "input_path"
        DATASET_SPLIT = "split"
