
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from dotenv import load_dotenv
import logging
import typer
from src.cli.interact.service import InteractService
from src.cli.missed_entities.service import MissEntitiesService
from src.cli.labelstudio_to_docbin.service import LabelStudioToDocbinService
from src.cli.export_data.service import ExportDataService
from src.cli.import_data.service import ImportService
from src.common.enums import DatasetSplit
from src.config.logging import setup_logging

load_dotenv()
app = typer.Typer()
logger = logging.getLogger(__name__)

@app.callback()
def main(debug: bool = typer.Option(False, help="Enable debug logging")):
    setup_logging(debug_mode=debug)
    logger.debug("Logging config: DEBUG")


@app.command(name="import")
def import_data(
        input_path: Path = typer.Option(..., "--input-path"),
        train_ratio: float = typer.Option(0.7, "--train-ratio"),
        val_ratio: float = typer.Option(0.2, "--val-ratio"),
        test_ratio: float = typer.Option(0.1, "--test-ratio"),
):
    """
    Split a dataset file into training, validation, and test sets.

    Takes a text file with one example per line and randomly splits it into 
    three separate files based on the provided ratios. Files are saved to 
    data/raw/training/, data/raw/validation/, and data/raw/testing/ directories
    with timestamped filenames.

    The original input file is deleted after successful splitting.

    Args:
        input_path: Path to the input file to split
        train_ratio: Fraction of data for training (default: 0.7)
        val_ratio: Fraction of data for validation (default: 0.2) 
        test_ratio: Fraction of data for testing (default: 0.1)
    """
    ratios = {
        "train_ratio": train_ratio,
        "val_ratio": val_ratio,
        "test_ratio": test_ratio,
    }
    ImportService.run(
        input_path=input_path, 
        ratios=ratios,
    )
    # SplitDataService.run(input_path=input_path, split=split)



@app.command(name="export-data")
def export_data():
    ExportDataService.run()


@app.command(name="labelstudio-to-docbin")
def labelstudio_to_docbin(
        input_path: Path = typer.Option(..., "--input-path"),
        split: DatasetSplit = typer.Option(..., "--split"),
):
    """
    Convert raw Label Studio JSON export into a spaCy DocBin file for model training.

    This command performs two steps:
    1. Converts the raw Label Studio export into spaCy-formatted JSON.
    2. Converts that cleaned JSON into a binary .spacy DocBin file.

    Both the intermediate JSON and final .spacy file are saved to disk,
    with timestamped filenames for traceability.

    Args:
        input_path: Path to the raw Label Studio export (.json)
        split: Dataset split type ( train / test / val )
    """
    LabelStudioToDocbinService.run(input_path=input_path, split=split)


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
    InteractService.run(inquiry=inquiry, model_dir=model_dir)


@app.command(name="missed_entities")
def missed_entities(input_path: Path = typer.Option(..., "--input-path")):
    MissEntitiesService.run(input_path=input_path)


if __name__ == "__main__":
    app()