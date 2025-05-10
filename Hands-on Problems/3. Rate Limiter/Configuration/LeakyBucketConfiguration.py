class LeakyBucketConfiguration:
    def __init__(self, leak_rate, interval, capacity):
        self.leak_rate = leak_rate
        self.capacity = capacity
        self.interval = interval

    def get_leak_rate(self):
        return self.leak_rate

    def get_capacity(self):
        return self.capacity

    def get_interval(self):
        return self.interval