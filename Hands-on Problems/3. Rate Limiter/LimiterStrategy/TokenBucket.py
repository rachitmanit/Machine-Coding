import threading
import time

from LimiterStrategy.AbstractLimiterStrategy import AbstractLimiterStrategy


class TokenBucket(AbstractLimiterStrategy):
    def __init__(self):
        self.users = dict()
        self._lock = threading.Lock()
        self._shutdown = threading.Event()
        self.refiller_thread = threading.Thread(target=self.refill_token)
        self.refiller_thread.start()

    def refill_token(self):
        while not self._shutdown.is_set():
            with self._lock:
                # 1. Fetching users is important because we can not take a lock on dict in forever running thread.
                #    Dict is thread safe which throws error if it is changed on same element like updates on
                #    remaining_tokens during refilling and reducing at same time.
                # 2. Doing list() is important as it creates a copy. Alone self.users.keys() is a live key view which
                #    can still throw error.
                users = list(self.users.keys())
            try:
                for user_id in users:
                    with self.users[user_id]["lock"]:
                        self._refill_token_for_user(user_id)
            except Exception as exp:
                print("Error while refilling tokens: {}".format(exp))
                time.sleep(0.1)

    def _refill_token_for_user(self, user_id):
        curr_time = time.time()
        elapsed_time = curr_time - self.users[user_id]["last_update_time"]
        interval = self.users[user_id]["config"].get_interval()
        capacity = self.users[user_id]["config"].get_capacity()
        if elapsed_time > interval:
            refill_rate = self.users[user_id]["config"].get_refill_rate_per_interval()
            tokens_to_add = int(elapsed_time / interval) * refill_rate
            self.users[user_id]["remaining_tokens"] = self.users[user_id]["remaining_tokens"] + tokens_to_add
            self.users[user_id]["remaining_tokens"] = min(capacity, self.users[user_id]["remaining_tokens"])

            # Use this for precision (recommended)
            self.users[user_id]["last_update_time"] += (tokens_to_add // refill_rate) * interval

            # Use this if precision is less critical (acceptable for interviews)
            # user["last_update_time"] = curr_time
            print("Refilling {} tokens for user: {} at curr_time: {}".format(refill_rate, user_id, curr_time))

    def is_allowed(self, user_id, timestamp=None):
        if user_id not in self.users:
            raise RuntimeError("User not registered")

        # return self.can_process_lazy(user_id)
        return self.can_process(user_id)

    def register_user(self, user_id, config):
        if user_id in self.users:
            print("User: {} is already registered".format(user_id))
            return

        if config is None:
            raise RuntimeError("config is None")
        with self._lock:
            self.users[user_id] = dict()
            self.users[user_id]["remaining_tokens"] = config.get_refill_rate_per_interval()
            self.users[user_id]["config"] = config
            self.users[user_id]["lock"] = threading.Lock()
            self.users[user_id]["last_update_time"] = time.time()

    def can_process(self, user_id):
        with self.users[user_id]["lock"]:
            if self.users[user_id]["remaining_tokens"] > 0:
                self.users[user_id]["remaining_tokens"] -= 1
                return True
            return False

    ##########################################################################################
    # Lazy refill implementation. Which is also correct but can be questioned for slowness.

    def lazy_refill_token(self, user_id):
        try:
            with self.users[user_id]["lock"]:
                self._refill_token_for_user(user_id)
        except Exception as exp:
            print("Error while refilling tokens: {}".format(exp))

    def can_process_lazy(self, user_id):
        self.lazy_refill_token(user_id)
        with self.users[user_id]["lock"]:
            if self.users[user_id]["remaining_tokens"] > 0:
                self.users[user_id]["remaining_tokens"] -= 1
                return True
            return False

    ##########################################################################################

    def shutdown(self):
        self._shutdown.set()
        self.refiller_thread.join()
        print("Shutting down TokenBucket")
