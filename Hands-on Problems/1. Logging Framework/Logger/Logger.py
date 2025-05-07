import threading
import time
from Helper.MetaSingleton import MetaSingleton
from .AbstractLogger import AbstractLogger
from .LogLevel import LogLevel

class Logger(AbstractLogger, metaclass=MetaSingleton):
    def __init__(self, output_handler, log_level=LogLevel.DEBUG):
        super().__init__(output_handler=output_handler, log_level=log_level)
        print("Initialised Logger....")
        self.format = "[{timestamp}] [{level}] {message}"
        self._lock = threading.Lock()

    def format_and_write(self, log_level_name, message):
        if not message or not self.output_handler:
            return
        text = self.format.format(timestamp=time.time(), level=log_level_name,
                                  message=message)
        with self._lock:
            self.output_handler.write(text)

    def debug(self, message):
        if self.log_level> LogLevel.DEBUG:
            return
        self.format_and_write(LogLevel.DEBUG.name, message)

    def info(self, message):
        if self.log_level> LogLevel.INFO:
            return
        self.format_and_write(LogLevel.INFO.name, message)

    def warn(self, message):
        if self.log_level> LogLevel.WARN:
            return
        self.format_and_write(LogLevel.WARN.name, message)

    def error(self, message):
        if self.log_level> LogLevel.ERROR:
            return
        self.format_and_write(LogLevel.ERROR.name, message)

    def set_output_handler(self, output_handler):
        with self._lock:
            self.output_handler = output_handler

    def set_log_level(self, log_level):
        with self._lock:
            self.log_level = log_level
