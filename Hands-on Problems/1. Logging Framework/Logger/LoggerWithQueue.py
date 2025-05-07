import queue
import threading
import time

from Helper.MetaSingleton import MetaSingleton
from .AbstractLogger import AbstractLogger
from .LogLevel import LogLevel


class LoggerQueueBased(AbstractLogger, metaclass=MetaSingleton):
    def __init__(self, output_handler, log_level=LogLevel.DEBUG):
        super().__init__(output_handler=output_handler, log_level=log_level)
        print("Initialised Logger....")
        self.format = "[{timestamp}] [{level}] {message}"
        self._lock = threading.Lock()
        self._queue = queue.Queue()
        self._shutdown = threading.Event()
        self.queue_thread = threading.Thread(target=self.process_queue)
        self.queue_thread.start()

    def process_queue(self):
        while not self._shutdown.is_set():
            try:
                log_level, message = self._queue.get(timeout=1)
                self.format_and_write(log_level, message)
            except queue.Empty:
                continue

    def format_and_write(self, log_level_name, message):
        if not message or not self.output_handler:
            return
        text = self.format.format(timestamp=time.time(), level=log_level_name,
                                  message=message)
        with self._lock:
            self.output_handler.write(text)

    def queue_message(self, log_level, message):
        self._queue.put((log_level, message))

    def debug(self, message):
        if self.log_level> LogLevel.DEBUG:
            return
        self.queue_message(LogLevel.DEBUG.name, message)

    def info(self, message):
        if self.log_level> LogLevel.INFO:
            return
        self.queue_message(LogLevel.INFO.name, message)

    def warn(self, message):
        if self.log_level> LogLevel.WARN:
            return
        self.queue_message(LogLevel.WARN.name, message)

    def error(self, message):
        if self.log_level> LogLevel.ERROR:
            return
        self.queue_message(LogLevel.ERROR.name, message)

    def set_output_handler(self, output_handler):
        with self._lock:
            self.output_handler = output_handler

    def set_log_level(self, log_level):
        with self._lock:
            self.log_level = log_level

    def shutdown(self):
        self._shutdown.set()
        self.queue_thread.join()
        print("queue_thread exited")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Inside LoggerWithQueue __exit__")
        self.shutdown()