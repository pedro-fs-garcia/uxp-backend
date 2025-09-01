import logging
import os
import json
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from queue import Queue
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": record.getMessage(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Se for erro, adiciona stacktrace
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)


class AsyncLogger:
    def __init__(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")

        formatter = JsonFormatter()

        max_file_size = 10 * 1024 * 1024  # 10MB
        backup_count = 5

        # Handlers de arquivo
        file_handler = RotatingFileHandler(
            "logs/app.json", maxBytes=max_file_size, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        error_handler = RotatingFileHandler(
            "logs/error.json", maxBytes=max_file_size, backupCount=backup_count, encoding="utf-8"
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)

        # Console (também em JSON)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)

        # Fila centralizada
        self.log_queue = Queue(-1)
        queue_handler = QueueHandler(self.log_queue)

        # Logger principal
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(queue_handler)

        # Listener roda em thread separada
        self.listener = QueueListener(
            self.log_queue,
            file_handler,
            error_handler,
            stream_handler,
        )
        self.listener.start()

    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(message, stacklevel=2, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        self.logger.info(message, stacklevel=2, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(message, stacklevel=2, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        self.logger.error(message, stacklevel=2, *args, **kwargs)

    def stop(self):
        self.listener.stop()


logger = AsyncLogger()
