import logging
import sys
from pathlib import Path
from colorlog import ColoredFormatter


def setup_logging(debug_mode: bool = False, log_file: Path = Path("log/error.log")) -> None:

    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Colorized terminal output
    color_formatter = ColoredFormatter(
        fmt="%(log_color)s%(levelname)-8s%(reset)s | %(name)s | %(message)s",
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        },
    )

    console_handler = logging.StreamHandler(sys.stdout)
    if debug_mode:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(color_formatter)

    # File output (ERROR and above, plain text)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    # Root logger config
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[console_handler, file_handler],
    )
