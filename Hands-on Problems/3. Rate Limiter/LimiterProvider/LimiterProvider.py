from enum import Enum, auto
from io import UnsupportedOperation

from LimiterStrategy.FixedWindowCounter import FixedWindowCounter
from LimiterStrategy.SlidingWindowLog import SlidingWindowLog


class LimiterType(Enum):
    FixedWindow = auto()
    SlidingLog = auto()

class LimitedProvider:
    @staticmethod
    def get_limiter(limiter_type):
        if limiter_type == LimiterType.FixedWindow:
            return FixedWindowCounter()
        elif limiter_type == LimiterType.SlidingLog:
            return SlidingWindowLog()

        raise NotImplementedError("Unsupported limiter_type: {}".format(limiter_type))