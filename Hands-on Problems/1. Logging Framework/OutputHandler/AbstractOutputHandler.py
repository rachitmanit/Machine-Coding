from abc import ABC, abstractmethod


class AbstractOutputHandler(ABC):

    @abstractmethod
    def write(self, text):
        pass

