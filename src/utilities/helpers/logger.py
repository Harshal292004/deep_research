from rich.console import Console
from rich.logging import RichHandler
import logging
import os


class Logger:
    def __init__(self, name: str, env: str = "development", log_file: str = "app.log"):
        self.env = env.lower()
        self.log_file = log_file
        self.logger = logging.getLogger(name)
        self._setup_logger()

    def _setup_logger(self):
        self.logger.setLevel(
            logging.DEBUG if self.env == "development" else logging.INFO
        )
        self.logger.handlers.clear()

        console = Console()

        # Console handler (Rich)
        console_handler = RichHandler(
            console=console,
            show_path=self.env == "development",
            show_time=True,
            show_level=True,
            rich_tracebacks=self.env == "development",
            markup=True,
        )
        console_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(console_formatter)

        # File handler with ANSI color codes
        file_handler = logging.FileHandler(self.log_file, mode="a")
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


log = Logger("Agent", env="development", log_file="app.log").get_logger()
