import logging.config
import queue
from pathlib import Path

from pydantic import BaseModel


class LogConfig(BaseModel):
    log_level: str = 'ERROR'
    formatter: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s -  %(lineno)d - %(filename)s'
    handler: str = "logging.handlers.RotatingFileHandler"
    path: Path = Path(__file__).parent.parent.parent / "logs"

    @property
    def get_log_config(self):
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": self.formatter,
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                },
            },
            "handlers": {
                "json_handler": {
                    "class": self.handler,
                    "formatter": "default",
                    "filename": self.path / 'logging.json',
                    "backupCount": 10,
                    "maxBytes": 200*1024*1024,

                }

            },
            "loggers": {
                "app": {
                    "handlers": ["json_handler"],
                    "level": self.log_level,

                }
            }
        }


