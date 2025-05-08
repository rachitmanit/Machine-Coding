from LimiterProvider.LimiterProvider import LimitedProvider

class LimiterService:

    def __init__(self, limiter_type):
        self.limiter = LimitedProvider.get_limiter(limiter_type)

    def register_user(self, user_id, config):
        self.limiter.register_user(user_id, config)

    def is_allowed(self, user_id, timestamp=None):
        return self.limiter.is_allowed(user_id, timestamp)
