import threading
import time

from LimiterStrategy.AbstractLimiterStrategy import AbstractLimiterStrategy


class SlidingWindowCounter(AbstractLimiterStrategy):

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
            self.users[user_id]["config"] = config
            self.users[user_id]["window"] = WindowManager(config.get_limit())

    def is_allowed(self, user_id, timestamp=None):
        if user_id not in self.users:
            raise RuntimeError("User not registered")

        return self.can_process(user_id)

    def can_process(self, user_id):
        if self.users[user_id]["window"].get_curr_request_in_interval(time.time()) < self.users[user_id]["config"].get_max_requests():
            self.users[user_id]["window"].incr_curr_window_requests()
            return True
        return False

class WindowManager:
    def __init__(self, request_interval):
        self.request_interval = request_interval
        curr_time = time.time()
        self.curr_window_start_time = curr_time
        self.curr_window_requests = 0
        self.prev_window_start_time = curr_time - request_interval
        self.prev_window_requests = 0

    def get_prev_window_requests(self):
        return self.prev_window_requests

    def get_prev_window_start_time(self):
        return self.prev_window_start_time

    def get_curr_window_requests(self):
        return self.curr_window_requests

    def get_curr_window_start_time(self):
        return self.curr_window_start_time

    def get_curr_request_in_interval(self, curr_time):
        self.update_windows(curr_time)
        fraction = (curr_time - self.curr_window_start_time) / self.request_interval
        curr_fraction = self.curr_window_requests * fraction
        prev_fraction = self.prev_window_requests * (1 - fraction)
        print("curr_fraction + prev_fraction: {}".format(curr_fraction + prev_fraction))
        return curr_fraction + prev_fraction

    def update_windows(self, curr_time):
        if curr_time - 2 * self.request_interval > self.curr_window_start_time:
            print("Coming here 1")
            self.reset_windows()
        elif curr_time - 2 * self.request_interval > self.prev_window_start_time:
            print("Coming here 2")
            self.prev_window_start_time = self.curr_window_start_time
            self.prev_window_requests = self.curr_window_requests
            self.curr_window_start_time = self.prev_window_start_time + self.request_interval
            self.curr_window_requests = 0

    def reset_windows(self):
        curr_time = time.time()
        self.curr_window_start_time = curr_time
        self.curr_window_requests = 0
        self.prev_window_start_time = curr_time - self.request_interval
        self.prev_window_requests = 0

    def incr_curr_window_requests(self):
        self.curr_window_requests += 1
        print(self.curr_window_requests)