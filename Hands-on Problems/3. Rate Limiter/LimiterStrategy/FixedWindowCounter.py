import threading
import time
from .AbstractLimiterStrategy import AbstractLimiterStrategy


class FixedWindowCounter(AbstractLimiterStrategy):

    def __init__(self):
        self.users = dict()
        self._lock = threading.Lock()

    def register_user(self, user_id, config):
        if user_id in self.users:
            print("User: {} is already registered".format(user_id))
            return

        if config is None:
            raise RuntimeError("config is None")
        with self._lock:
            self.users[user_id] = dict()
            self.users[user_id]["requests"] = 0
            self.users[user_id]["config"] = config
            self.users[user_id]["window_start"] = time.time()
            self.users[user_id]["lock"] = threading.Lock()

    def is_allowed(self, user_id, timestamp=None):
        if user_id not in self.users:
            raise RuntimeError("User not registered")

        return self.can_process(user_id)

    def update_window(self, user_id):
        with self.users[user_id]["lock"]:
            if time.time() - self.users[user_id]["window_start"] > self.users[user_id]["config"].get_limit():
                self.users[user_id]["requests"] = 0
                self.users[user_id]["window_start"] = time.time()

    def can_process(self, user_id):
        self.update_window(user_id)
        with self.users[user_id]["lock"]:
            if self.users[user_id]["requests"] < self.users[user_id]["config"].get_max_requests():
                self.users[user_id]["requests"] += 1
                return True
        return False
