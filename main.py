
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import typer
from src.cli.build_docbin import DocBinBuilder
from src.cli.label_studio_converter import LabelStudioConverter
from src.common.io import FileManager
from src.config.config import DATA_DIR
from src.config.logging import setup_logging


app = typer.Typer()


@app.callback()
def main(debug: bool = typer.Option(False, help="Enable debug logging")):
    setup_logging(debug_mode=debug)


@app.command(name="convert-labels")
def convert_labels(input_path: Path):
    output_dir = DATA_DIR / "converted"
    file_manager = FileManager(output_dir)
    converter = LabelStudioConverter(file_manager)
    converter.convert(input_path)


@app.command(name="build-docbin")
def build_docbin(input_path: Path):
    output_dir = DATA_DIR / "spacy"
    file_manager = FileManager(output_dir)
    builder = DocBinBuilder(file_manager)
    builder.build_docbin(input_path)


if __name__ == "__main__":
    app()