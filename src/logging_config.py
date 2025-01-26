from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter

def setup_logging(debug: bool, base_dir: Path):
    # Ensure base_dir is a Path object
    if not isinstance(base_dir, Path):
        base_dir = Path(base_dir)

    # Create log directory if it doesn't exist
    log_dir = base_dir / "log"
    log_dir.mkdir(parents=True, exist_ok=True)

    # File handler (WARNING and above)
    file_handler = RotatingFileHandler(
        filename=str(log_dir / "error.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Console handler (DEBUG/INFO and above based on `debug`)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(
        ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "white",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    )

    # Root logger configuration
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, console_handler],
    )
