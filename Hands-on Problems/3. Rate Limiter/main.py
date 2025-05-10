import time
from traceback import print_tb

from Configuration.LeakyBucketConfiguration import LeakyBucketConfiguration
from Configuration.TokenBucketConfiguration import TokenBucketConfiguration
from Configuration.WindowLimiterConfiguration import WindowLimiterConfiguration
from LimiterProvider.LimiterProvider import LimiterType, AsyncLimiterType
from LimiterService.LimiterService import LimiterService, AsyncLimiterService
from LimiterStrategy.LeakyBucket import LeakyBucket


def test_fixed_window():
    ls = LimiterService(LimiterType.FixedWindow)
    user_id1 = 1
    ls.register_user(user_id1, WindowLimiterConfiguration(5, 1))
    for i in range(6):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id1)))

    print("----------------------------------")

    user_id1 = 2
    ls.register_user(user_id1, WindowLimiterConfiguration(10, 10))
    for i in range(16):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id1)))


    print("----------------------------------")
    print("End of Test case")
    print("----------------------------------")

def test_sliding_window_log():
    ls = LimiterService(LimiterType.SlidingLog)
    user_id1 = 1
    ls.register_user(user_id1, WindowLimiterConfiguration(5, 1))
    for i in range(6):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id1)))

    print("----------------------------------")

    user_id1 = 2
    ls.register_user(user_id1, WindowLimiterConfiguration(10, 10))
    for i in range(16):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id1)))


    print("----------------------------------")
    print("End of Test case")
    print("----------------------------------")

def test_token_bucket():
    ls = LimiterService(LimiterType.TokenBucket)
    user_id1 = 1
    ls.register_user(user_id1, TokenBucketConfiguration(2, 10, 4))
    for i in range(6):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id1)))

    print("----------------------------------")

    user_id2 = 2
    ls.register_user(user_id2, TokenBucketConfiguration(10, 10, 15))
    for i in range(16):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id2)))

    print("Sleeping for 1 second before retrying...")
    time.sleep(1)
    print("Trying again for user_id: {}".format(user_id2))
    for i in range(5):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id2)))

    print("Sleeping for 10 second before retrying...")
    time.sleep(10)
    print("Trying again for user_id: {}".format(user_id2))
    for i in range(15):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id2)))

    ls.limiter.shutdown()

    print("----------------------------------")
    print("End of Test case")
    print("----------------------------------")

def test_leaky_bucket():
    ls = AsyncLimiterService(AsyncLimiterType.LeakyBucket)
    user_id1 = 1
    ls.register_user(user_id1, LeakyBucketConfiguration(2, 5, 5))
    for i in range(6):
        print("User: {} request {} accepted : {}".format(user_id1, i, ls.submit(user_id1, i)))

    print("Sleeping to observe task processing in Rate Limiter's Queue")
    time.sleep(6)

    print("----------------------------------")

    user_id2 = 2
    ls.register_user(user_id2, LeakyBucketConfiguration(10, 10, 15))
    for i in range(16):
        print("User: {} request {} accepted : {}".format(user_id2, i, ls.submit(user_id2, i)))

    print("Sleeping for 1 second before retrying...")
    time.sleep(1)
    print("Trying again for user_id: {}".format(user_id2))
    for i in range(5):
        print("User: {} request {} accepted : {}".format(user_id2, i, ls.submit(user_id2, i)))

    print("Sleeping to observe all queued task processing in Rate Limiter's Queue")
    time.sleep(30)

    ls.limiter.shutdown()

    print("----------------------------------")
    print("End of Test case")
    print("----------------------------------")

if __name__ == '__main__':

    # test_fixed_window()

    # test_sliding_window_log()

    # test_token_bucket()

    test_leaky_bucket()