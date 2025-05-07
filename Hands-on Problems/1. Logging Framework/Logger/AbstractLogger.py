from abc import ABC, abstractmethod

class AbstractLogger(ABC):

    def __init__(self, output_handler, log_level):
        self.output_handler = output_handler
        self.log_level = log_level

    @abstractmethod
    def debug(self, message):
        pass

    @abstractmethod
    def info(self, message):
        pass

    @abstractmethod
    def warn(self, message):
        pass

    @abstractmethod
    def error(self, message):
        pass

    @abstractmethod
    def set_output_handler(self, output_handler):
        pass

    @abstractmethod
    def set_log_level(self, log_level):
        pass
