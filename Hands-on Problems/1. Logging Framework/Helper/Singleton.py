import threading


class Singleton:
    def __init__(self, cls):
        self._instance = None
        self.cls = cls
        self.lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            with self.lock:
                if self._instance is None:
                    self._instance = self.cls(*args, **kwargs)
        return self._instance
