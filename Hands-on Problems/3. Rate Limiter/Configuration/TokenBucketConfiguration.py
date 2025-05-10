class TokenBucketConfiguration:

    def __init__(self, refill_rate_per_interval, interval, capacity):
        self.refill_rate_per_interval = refill_rate_per_interval
        self.interval = interval
        self.capacity = capacity

    def get_refill_rate_per_interval(self):
        return self.refill_rate_per_interval

    def get_interval(self):
        return self.interval

    def get_capacity(self):
        return self.capacity
