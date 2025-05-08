class LimiterConfiguration:

    def __init__(self, limit, max_requests):
        self.limit = limit
        self.max_requests = max_requests

    def update_limit(self, limit):
        self.limit = limit

    def update_max_requests(self, max_requests):
        self.max_requests = max_requests

    def get_max_requests(self):
        return self.max_requests

    def get_limit(self):
        return self.limit
