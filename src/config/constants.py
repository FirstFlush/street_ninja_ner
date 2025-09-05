from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = DATA_DIR / "training" / "model-best"

RAW_DIR = DATA_DIR / "raw"
RAW_TRAINING_DIR = RAW_DIR / "training"
RAW_VALIDATION_DIR = RAW_DIR / "validation"
RAW_TESTING_DIR = RAW_DIR / "testing"