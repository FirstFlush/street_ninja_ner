from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = DATA_DIR / "training" / "model-best"