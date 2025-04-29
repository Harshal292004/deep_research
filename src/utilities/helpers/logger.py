from rich.console import Console
from rich.logging import RichHandler
import logging
import os

class Logger:
    def __init__(self, name: str, env: str = "development"):
        self.name = name
        self.env = env.lower()
        self.logger = logging.getLogger(name)
        self._setup_logger()

    def _setup_logger(self):
        self.logger.setLevel(
            logging.DEBUG if self.env == "development" else logging.INFO
        )
        self.logger.handlers.clear()

        console = Console()

        handler = RichHandler(
            console=console,
            show_path=self.env == "development",
            show_time=True,
            show_level=True,
            rich_tracebacks=True if self.env == "development" else False,
            markup=True,
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger


log = Logger("Agent").get_logger()
