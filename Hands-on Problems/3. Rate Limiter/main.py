import time

from Configuration.LimiterConfiguration import LimiterConfiguration
from LimiterProvider.LimiterProvider import LimiterType
from LimiterService.LimiterService import LimiterService

def test_fixed_window():
    ls = LimiterService(LimiterType.FixedWindow)
    user_id1 = 1
    ls.register_user(user_id1, LimiterConfiguration(5, 1))
    for i in range(6):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id1)))

    print("----------------------------------")

    user_id1 = 2
    ls.register_user(user_id1, LimiterConfiguration(10, 10))
    for i in range(16):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id1)))


    print("----------------------------------")
    print("End of Test case")
    print("----------------------------------")

def test_sliding_window_log():
    ls = LimiterService(LimiterType.SlidingLog)
    user_id1 = 1
    ls.register_user(user_id1, LimiterConfiguration(5, 1))
    for i in range(6):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id1)))

    print("----------------------------------")

    user_id1 = 2
    ls.register_user(user_id1, LimiterConfiguration(10, 10))
    for i in range(16):
        print("User request {} allowed : {}".format(i, ls.is_allowed(user_id1)))


    print("----------------------------------")
    print("End of Test case")
    print("----------------------------------")

if __name__ == '__main__':

    # test_fixed_window()

    test_sliding_window_log()