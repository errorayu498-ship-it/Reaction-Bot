import logging
from colorlog import ColoredFormatter

def setup_logger():

    handler = logging.StreamHandler()

    formatter = ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    handler.setFormatter(formatter)

    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


logger = setup_logger()
