import threading
import time

from Configuration.LimiterConfiguration import LimiterConfiguration
from .AbstractStrategy import AbstractStrategy


class SlidingWindowLog(AbstractStrategy):

    def __init__(self):
        self.users = dict()
        self._lock = threading.Lock()

    def register_user(self, user_id, config):
        if config is None:
            raise RuntimeError("config is None")
        with self._lock:
            self.users[user_id] = dict()
            self.users[user_id]["requests"] = list()
            self.users[user_id]["config"] = config
            self.users[user_id]["lock"] = threading.Lock()

    def is_allowed(self, user_id, timestamp=None):
        if user_id not in self.users:
            raise RuntimeError("User not registered")

        return self.can_process(user_id)

    def update_window(self, user_id):
        with self.users[user_id]["lock"]:
            idx = 0
            curr_time = time.time()
            while idx < len(self.users[user_id]["requests"]) and \
                    self.users[user_id]["requests"][idx] < curr_time - self.users[user_id]["config"].get_limit():
                idx += 1
            if idx == len(self.users[user_id]["requests"]):
                self.users[user_id]["requests"] = list()
            else:
                self.users[user_id]["requests"] = self.users[user_id]["requests"][idx:]

    def can_process(self, user_id):
        self.update_window(user_id)
        with self.users[user_id]["lock"]:
            self.users[user_id]["requests"].append(time.time())
            if len(self.users[user_id]["requests"]) <= self.users[user_id]["config"].get_max_requests():
                return True
        return False