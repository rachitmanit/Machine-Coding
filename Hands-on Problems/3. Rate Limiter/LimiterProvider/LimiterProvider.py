from enum import Enum, auto

from LimiterStrategy.FixedWindowCounter import FixedWindowCounter
from LimiterStrategy.LeakyBucket import LeakyBucket
from LimiterStrategy.SlidingWindowCounter import SlidingWindowCounter
from LimiterStrategy.SlidingWindowLog import SlidingWindowLog
from LimiterStrategy.TokenBucket import TokenBucket


class LimiterType(Enum):
    FixedWindow = auto()
    SlidingLog = auto()
    TokenBucket = auto()
    SlidingWindowCounter = auto()

class AsyncLimiterType(Enum):
    LeakyBucket = auto()

class LimitedProvider:
    @staticmethod
    def get_limiter(limiter_type):
        if limiter_type == LimiterType.FixedWindow:
            return FixedWindowCounter()
        elif limiter_type == LimiterType.SlidingLog:
            return SlidingWindowLog()
        elif limiter_type == LimiterType.TokenBucket:
            return TokenBucket()
        elif limiter_type == LimiterType.SlidingWindowCounter:
            return SlidingWindowCounter()

        raise NotImplementedError("Unsupported limiter_type: {}".format(limiter_type))

    @staticmethod
    def get_async_limiter(limiter_type):
        if limiter_type == AsyncLimiterType.LeakyBucket:
            return LeakyBucket()

        raise NotImplementedError("Unsupported async limiter_type: {}".format(limiter_type))