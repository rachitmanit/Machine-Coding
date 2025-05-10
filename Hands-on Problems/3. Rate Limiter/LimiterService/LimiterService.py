from LimiterProvider.LimiterProvider import LimitedProvider

class LimiterService:

    def __init__(self, limiter_type):
        self.limiter = LimitedProvider.get_limiter(limiter_type)

    def register_user(self, user_id, config):
        self.limiter.register_user(user_id, config)

    def is_allowed(self, user_id, timestamp=None):
        return self.limiter.is_allowed(user_id, timestamp)

# This is Bonus implementation as it is less likely to be asked.
# Also, this is different from original LimiterService limiters as per
# original Problem Statement.txt.
# Improvisation: We could have built a BaseLimiterService and move
# register_user to it, but then it would look like a project instead of
# enhanced Machine Coding problem. Like: AsyncLimiterService(BaseClass...)
class AsyncLimiterService:

    def __init__(self, limiter_type):
        self.limiter = LimitedProvider.get_async_limiter(limiter_type)

    def register_user(self, user_id, config):
        self.limiter.register_user(user_id, config)

    def submit(self, user_id, task):
        return self.limiter.submit(user_id, task)