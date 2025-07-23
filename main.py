
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import logging
import typer
from src.cli.services.docbin import DocbinService
from src.cli.services.label_studio_converter import LabelStudioService
from src.cli.services.interact import InteractService
from src.cli.services.missed_entities import MissEntitiesService
from src.config.logging import setup_logging


app = typer.Typer()
logger = logging.getLogger(__name__)

@app.callback()
def main(debug: bool = typer.Option(False, help="Enable debug logging")):
    setup_logging(debug_mode=debug)
    logger.debug("Logging config: DEBUG")


@app.command(name="convert-labels")
def convert_labels(input_path: Path = typer.Option(..., "--input-path")):
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
    LabelStudioService.run(input_path=input_path)


@app.command(name="docbin")
def docbin(input_path: Path = typer.Option(..., "--input-path")):
    """
    Convert spaCy-formatted JSON into a .spacy DocBin file.

    This command takes preprocessed training data (with text and entity spans)
    and converts it into a binary spaCy DocBin file used for model training.

    Args:
        input_path: Path to the cleaned JSON file (from `convert-labels`)
    """
    DocbinService.run(input_path=input_path)


@app.command(name="interact")
def interact(
    inquiry: str,
    model_dir: Path = typer.Option(None, help="Path to trained model directory. model-last/ will be used as default.")
):
    """
    Run an input string through the trained NER model and print extracted entities.

    This command is designed for quick, interactive testing of the trained model
    using real or test SMS-style messages. It loads the latest trained spaCy model,
    runs inference, and prints out detected entities and their labels.

    Args:
        inquiry: A single text input to parse (e.g., "where's shelter near 222 main st?").
    """
    InteractService.run(inquiry=inquiry, model_path=model_dir)


@app.command(name="missed_entities")
def missed_entities(input_path: Path = typer.Option(..., "--input-path")):
    MissEntitiesService.run(input_path=input_path)


if __name__ == "__main__":
    app()