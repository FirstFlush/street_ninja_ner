#!/usr/bin/env python3

import click
from pathlib import Path
from src.preprocess import Preprocessor
from src.config import DATA_DIR


@click.group()
def cli():
    """CLI for managing ML tasks in Street Ninja."""
    pass


@click.command()
@click.option(
    "--input", "-i", 
    required=True, 
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, allow_dash=True),
    help="Path to the raw Label Studio JSON file (relative to ml/ directory)"
)
def preprocess(input):
    """
    Preprocess raw Label Studio JSON into spaCy-compatible .spacy format.
    """
    # Resolve the input path relative to the ml/ directory
    input_path = Path(input).name  # Ensure it's the filename
    preprocessor = Preprocessor(input_file=input_path, DATA_DIR=DATA_DIR)
    preprocessor.preprocess_label_studio_data()
    click.echo(f"Preprocessed data saved to {DATA_DIR / 'processed'}")



# Add commands to the CLI group
cli.add_command(preprocess)

if __name__ == "__main__":
    cli()
