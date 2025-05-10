from abc import ABC, abstractmethod


class AbstractLimiterStrategy(ABC):

    @abstractmethod
    def is_allowed(self, user_id, timestamp=None): pass

    @abstractmethod
    def register_user(self, user_id, config): pass

class AbstractAsyncLimiterStrategy(ABC):

    @abstractmethod
    def submit(self, user_id, task): pass

    @abstractmethod
    def register_user(self, user_id, config): pass