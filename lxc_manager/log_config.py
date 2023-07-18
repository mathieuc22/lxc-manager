import logging
import sys

import colorlog


def setup_logging(log_level: str):
    log_level = getattr(logging, log_level.upper(), "INFO")

    log_format = "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    # Configuration de colorlog
    colored_formatter = colorlog.ColoredFormatter(
        log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )

    # Configuration du gestionnaire de log
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(colored_formatter)

    # Configuration du logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(handler)
