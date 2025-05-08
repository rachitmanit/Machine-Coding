from abc import ABC, abstractmethod


class AbstractChannel(ABC):

    @abstractmethod
    def notify(self, user, content): pass