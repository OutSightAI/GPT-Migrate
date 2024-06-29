import logging
import sys


def setup_logger(name, level=logging.INFO):
    """Set up a logger with the given name and level."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Create a formatting for the logs
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


# Create a default logger for the entire application
app_logger = setup_logger("gpt_migrate")
