import threading
import time

from Helper.Singleton import Singleton
from .AbstractLogger import AbstractLogger
from .LogLevel import LogLevel

@Singleton
class Logger(AbstractLogger):
    def __init__(self, output_handler, log_level):
        super().__init__(output_handler=output_handler, log_level=log_level)
        print("Initialised Logger....")
        self.format = "[{timestamp}] [{level}] {message}"
        self._lock = threading.Lock()

    def format_and_write(self, log_level_name, message):
        text = self.format.format(timestamp=time.time(), level=log_level_name,
                                  message=message)
        with self._lock:
            self.output_handler.write(text)

    def debug(self, message):
        if LogLevel.DEBUG < self.log_level:
            return
        self.format_and_write(LogLevel.DEBUG.name, message)

    def info(self, message):
        if LogLevel.INFO < self.log_level:
            return
        self.format_and_write(LogLevel.INFO.name, message)

    def warn(self, message):
        if LogLevel.WARN < self.log_level:
            return
        self.format_and_write(LogLevel.WARN.name, message)

    def error(self, message):
        if LogLevel.ERROR < self.log_level:
            return
        self.format_and_write(LogLevel.ERROR.name, message)

    def set_output_handler(self, output_handler):
        self.output_handler = output_handler

    def set_log_level(self, log_level):
        self.log_level = log_level
