import time

class ExponentialRetry:

    @staticmethod
    def exponential_retry(func, max_retries=5, max_delay=10, base_delay=1, args=(), kwargs=None):

        if kwargs is None:
            kwargs = {}

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as exp:
                wait = min(base_delay * (2 ** attempt), max_delay)
                print("Retrying Function: {}. Attempt: {}. Exception: {}".format(func.__name__, attempt, exp))
                time.sleep(wait)

        raise Exception("All retries to Function: {} failed".format(func.__name__))
