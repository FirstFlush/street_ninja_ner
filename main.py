
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import logging
import typer
from src.cli.build_docbin import DocBinBuilder
from src.cli.label_studio_converter import LabelStudioConverter
from src.cli.interact import InteractionClient
from src.common.io import FileManager
from src.config.constants import DATA_DIR
from src.config.logging import setup_logging


app = typer.Typer()
logger = logging.getLogger(__name__)

@app.callback()
def main(debug: bool = typer.Option(False, help="Enable debug logging")):
    setup_logging(debug_mode=debug)
    logger.debug("Logging config: DEBUG")


@app.command(name="convert-labels")
def convert_labels(input_path: Path):
    """
    Convert raw Label Studio JSON to spaCy-formatted JSON.

    This command reads the messy, nested annotation output from Label Studio
    and converts it into a clean list of training examples that spaCy can understand.

    Output format:
      [
        {
          "text": "Need to pee near Olympic Village",
          "entities": [[8, 11, "RESOURCE"], [17, 32, "LOCATION"]]
        },
        ...
      ]

    Args:
        input_path: Path to the raw Label Studio export (.json)
    """
    output_dir = DATA_DIR / "converted"
    file_manager = FileManager(output_dir)
    converter = LabelStudioConverter(file_manager)
    converter.convert(input_path)


@app.command(name="build-docbin")
def build_docbin(input_path: Path):
    """
    Convert spaCy-formatted JSON into a .spacy DocBin file.

    This command takes preprocessed training data (with text and entity spans)
    and converts it into a binary spaCy DocBin file used for model training.

    Args:
        input_path: Path to the cleaned JSON file (from `convert-labels`)
    """
    output_dir = DATA_DIR / "spacy"
    file_manager = FileManager(output_dir)
    builder = DocBinBuilder(file_manager)
    builder.build_docbin(input_path)


@app.command(name="interact")
def interact(inquiry: str):
    """
    Run an input string through the trained NER model and print extracted entities.

    This command is designed for quick, interactive testing of the trained model
    using real or test SMS-style messages. It loads the latest trained spaCy model,
    runs inference, and prints out detected entities and their labels.

    Args:
        inquiry: A single text input to parse (e.g., "need food near main and hastings").
    """
    stripped_inquiry = inquiry.strip()
    if not 1 <= len(stripped_inquiry) <= 256:
        logger.error(f"Inquiry length `{len(stripped_inquiry)}` invalid. Must be between 1 <= 256 chars.")
        typer.Exit(code=1)
    else:
      client = InteractionClient()
      client.print_entities(inquiry)


if __name__ == "__main__":
    app()