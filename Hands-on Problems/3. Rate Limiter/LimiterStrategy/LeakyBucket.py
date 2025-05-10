import queue
import threading
import time

from LimiterStrategy.AbstractLimiterStrategy import AbstractAsyncLimiterStrategy


class LeakyBucket(AbstractAsyncLimiterStrategy):

    def __init__(self):
        self.users = dict()
        self._lock = threading.Lock()
        self._shutdown = threading.Event()
        self._process_thread = threading.Thread(target=self._process_queue)
        self._process_thread.start()

    def _process_queue(self):
        while not self._shutdown.is_set():
            with self._lock:
                users = list(self.users.keys())
            for user in users:
                self._process_user_queue(user)

    def _process_user_queue(self, user_id):
        curr_time = time.time()
        last_leak_time = self.users[user_id]["last_leak_time"]
        elapsed_time = curr_time - last_leak_time
        interval = self.users[user_id]["config"].get_interval()
        leak_rate = self.users[user_id]["config"].get_leak_rate()
        if elapsed_time > interval:
            processed = False
            while not self.users[user_id]["queue"].empty() and leak_rate > 0:
                processed = True
                print("Processing for user: {} with leak_rate: {}".format(user_id, leak_rate))
                task = self.users[user_id]["queue"].get()
                self._process_task(user_id, task)
                leak_rate -= 1
            if processed:
                self.users[user_id]["last_leak_time"] = curr_time


    def _process_task(self, user_id, task):
        print("Processing Task: {} for user: {}".format(task, user_id))

    def register_user(self, user_id, config):
        if user_id in self.users:
            print("User: {} is already registered".format(user_id))
            return

        if config is None:
            raise RuntimeError("config is None")
        with self._lock:
            self.users[user_id] = dict()
            self.users[user_id]["config"] = config
            # self.users[user_id]["lock"] = threading.Lock()
            # Queue is thread safe.
            # We do not require explicit locks to carry out put and get
            self.users[user_id]["queue"] = queue.Queue()

            # Requests queued right after registration will be picked after "interval"
            # seconds
            self.users[user_id]["last_leak_time"] = time.time()

    def submit(self, user_id, task):
        if user_id not in self.users:
            raise RuntimeError("User: {} not registered.".format(user_id))

        if self.users[user_id]["config"].get_capacity() > self.users[user_id]["queue"].qsize():
            self.users[user_id]["queue"].put(task)
            return True
        else:
            return False

    def shutdown(self):
        self._shutdown.set()
        self._process_thread.join()
        print("Shutting down process thread")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()