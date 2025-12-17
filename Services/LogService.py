import logging
from pathlib import Path

class LogService:
    _initialized = False

    @staticmethod
    def init():
        if LogService._initialized:
            return

        log_dir = Path.home() / "Documents" / "Farm"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "game.log"

        logging.basicConfig(
            level=logging.INFO,
            format="{asctime} - {levelname} - {name} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
            handlers=[logging.FileHandler(log_file, mode="a", encoding="utf-8"), logging.StreamHandler()]
        )

        LogService._initialized = True