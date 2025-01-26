#!/usr/bin/env python3

import click
import logging
from src.config import DATA_DIR, DEBUG, BASE_DIR, DEFAULT_MODEL
from src.logging_config import setup_logging
from src.common.enums import ModelType
from src.cli import CLIHandler


# Set up logging
setup_logging(debug=DEBUG, base_dir=BASE_DIR)
logger = logging.getLogger(__name__)

# Instantiate CLIHandler with default model type (spaCy)
default_model_type = ModelType(DEFAULT_MODEL)
cli_handler = CLIHandler(model_type=default_model_type)

# Main CLI group
@click.group()
def cli():
    """CLI for managing ML tasks in Street Ninja."""
    pass


# Preprocess command
@click.command()
@click.option(
    "--dataset-type", "-d",
    required=True,
    type=click.Choice(["training", "validation"], case_sensitive=False),
    help="Specify the type of dataset being preprocessed (e.g., training or validation)."
)
@click.option(
    "--model", "-m",
    default="spacy",
    show_default=True,
    type=click.Choice(["spacy", "hugging_face"], case_sensitive=False),
    help="Specify the model type for preprocessing (e.g., spacy or hugging_face)."
)
@click.option(
    "--list-raw", "-l",
    is_flag=True,
    help="List raw files available for preprocessing."
)
@click.option(
    "--clean", "-c",
    is_flag=True,
    help="Clean processed files before preprocessing."
)
def preprocess(model:str, dataset_type:str, list_raw:bool, clean:bool):
    """
    Preprocess raw data into the format required by the specified model.
    """
    cli_preprocessor = cli_handler.build_preprocessor(
        model=model,
        dataset_type=dataset_type,
    )
    if list_raw:
        raw_files = cli_preprocessor.list_raw_files()
        if raw_files:
            logger.info("Raw Files:")
            for file in raw_files:
                logger.info(f"{file}")
        else:
            logger.info("No raw files found.")
        return

    if clean:
        cli_preprocessor.clean_processed()
        logger.info("Processed files cleaned.")

    cli_preprocessor.preprocess()
    logger.info(f"Preprocessing complete. Processed data saved to {DATA_DIR / 'processed' / dataset_type}")


# Train command (placeholder)
@click.command()
@click.option(
    "--train-file", "-tf",
    type=click.Path(exists=True, file_okay=True),
    help="Path to the processed training .spacy file."
)
@click.option(
    "--dev-file", "-df",
    type=click.Path(exists=True, file_okay=True),
    help="Path to the processed validation .spacy file."
)
def train(train_file, dev_file):
    """
    Train a spaCy model with the latest or specified data files.
    """
    logger.info("Training is not yet fully implemented.")


# Add commands to the CLI group
cli.add_command(preprocess)
cli.add_command(train)


if __name__ == "__main__":
    cli()
