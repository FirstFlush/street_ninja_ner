from pathlib import Path



DEBUG = False  # False sets terminal log level to INFO

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
MODEL_LAST = OUTPUT_DIR / "model-last"
MODEL_BEST = OUTPUT_DIR / "model-best"


class Defaults:
    OUTPUT_DIR = "output"
    MODEL = "spacy"
    CONFIG_PATH = "config.cfg"