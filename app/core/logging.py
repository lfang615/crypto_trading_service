import logging
import sys
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_entry)

class AsyncLogHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def emit(self, record):
        log_entry = self.format(record)
        sys.stdout.write(log_entry + "\n")
        sys.stdout.flush()

class AsyncLogger:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def emit(self, record):
        log_entry = self.format(record)
        sys.stdout.write(log_entry + "\n")
        sys.stdout.flush()

class AsyncLogger:
    _instance = None

    def __new__(cls, name: str = None, level: str = logging.INFO):
        if cls._instance is None:
            cls._instance = super(AsyncLogger, cls).__new__(cls)
            cls._instance.logger = cls._initialize_logger(name, level)
        return cls._instance

    @staticmethod
    def _initialize_logger(name: str, level: str = logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Console log handler
        ch = AsyncLogHandler()
        ch.setLevel(level)
        formatter = JSONFormatter()
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        return logger

    def get_logger(self):
        return self.logger

# Usage:
# logger = AsyncLogger(__name__).get_logger()
# logger.info("This is an info message")
