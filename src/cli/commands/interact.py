from enum import Enum
import logging
from pathlib import Path
import spacy
from .base import BaseCommand
from ...config.constants import MODEL_DIR


logger = logging.getLogger(__name__)


class InteractCommand(BaseCommand):
    """
    A simple interface for loading a trained spaCy NER model and parsing
    freeform text inputs, such as SMS-style inquiries.

    Designed for CLI-based interaction and debugging, this class provides
    utilities to:
    - Load a trained pipeline from a specified path
    - Extract and return named entities from user input
    - Pretty-print results for fast manual inspection

    Usage:
        ner = InteractionClient("data/training/model-best")
        ner.print_entities("need shelter near main and hastings")
    """

    class Args(Enum):
        INQUIRY = "inquiry"

    class Kwargs(Enum):
        MODEL_PATH = "model_path"

    def __init__(self, model_path: Path = MODEL_DIR):
        if not model_path.exists():
            msg = f"Model not found: {model_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)
        self.nlp = spacy.load(model_path)

    def parse(self, inquiry: str) -> list[tuple[str, str]]:
        """
        Returns a list of (entity_text, entity_label) for the given input text.
        """
        doc = self.nlp(inquiry)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def parse_and_print(self, text: str) -> None:
        """
        Prints labeled entities for interactive CLI usage.
        """
        results = self.parse(text)
        if not results:
            logger.info("No entities found")
            return
        for ent_text, label in results:
            print(f"{label:10} | {ent_text}")
