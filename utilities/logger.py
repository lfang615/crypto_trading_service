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
    def __init__(self, name: str, level: str = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Console log handler
        ch = AsyncLogHandler()
        ch.setLevel(level)
        formatter = JSONFormatter()
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

# Usage:
# logger = AsyncLogger(__name__).get_logger()
# logger.info("This is an info message")
