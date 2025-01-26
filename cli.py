#!/usr/bin/env python3

import click
import logging
from src.config import DATA_DIR, DEBUG, BASE_DIR, Defaults
from src.logging_config import setup_logging
from src.common.enums import ModelType
from src.cli import CLIHandler


# Set up logging
setup_logging(debug=DEBUG, base_dir=BASE_DIR)
logger = logging.getLogger(__name__)

cli_handler = CLIHandler()

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
    type=click.Choice(cli_handler.DATASET_TYPE_CHOICES, case_sensitive=False),
    help="Specify the type of dataset being preprocessed (e.g., training or validation)."
)
@click.option(
    "--model", "-m",
    default="spacy",
    show_default=True,
    type=click.Choice(cli_handler.MODEL_CHOICES, case_sensitive=False),
    help="Specify the model type for preprocessing (e.g., spacy or hugging_face)."
)
@click.option(
    "--list-raw", "-l",
    is_flag=True,
    help="List raw files available for preprocessing."
)

def preprocess(model:str, dataset_type:str, list_raw:bool):
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

    cli_preprocessor.preprocess()
    logger.info(f"Preprocessing complete. Processed data saved to {DATA_DIR / 'processed' / dataset_type}")


# Training command
@click.command()
@click.option(
    "--model", "-m",
    default=None,
    type=click.Choice(cli_handler.MODEL_CHOICES, case_sensitive=False),
    help="Specify the model type for training (e.g., spacy or hugging_face). Defaults to default model defined in config.py."
)
@click.option(
    "--config", "-c",
    default=None,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Path to the config file. Defaults to './config.cfg'."
)
@click.option(
    "--output", "-o",
    default=None,
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    help="Path to save the trained model. Defaults to './output/'."
)
def train(model:str, config:str, output:str):
    """
    Train a model.
    """
    logger.info("Building training config object..")
    cli_training = cli_handler.build_training(
        model=model,
        config_path=config,
        output_dir=output,
    )
    logger.info(f"Training config: `{cli_training.config}`")
    cli_training.train()
    logger.info("Training complete!")



# Add commands to the CLI group
cli.add_command(preprocess)
cli.add_command(train)


if __name__ == "__main__":
    cli()
