import traceback

from Channels.ChannelTypes import ChannelTypes
from NotificationService.NotificationService import NotificationService
from User.User import User

def test_notifications():
    rachit = User("Rachit", "a@gmail.com", "123456", "apple_15")
    deepanshi = User("Deepanshi", "b@gmail.com", "234567", "pixel_9")
    ns = NotificationService()
    ns.register_user(rachit)
    ns.register_user(deepanshi)

    ns.subscribe_channel(rachit.name, ChannelTypes.SMS)
    ns.subscribe_channel(rachit.name, ChannelTypes.PUSH)

    ns.subscribe_channel(deepanshi.name, ChannelTypes.EMAIL)
    ns.subscribe_channel(deepanshi.name, ChannelTypes.PUSH)

    print("Only SMS:")
    ns.notify(
        [rachit.name, deepanshi.name],
        [ChannelTypes.SMS],
        "Hello There")

    print("---------------------------------")

    print("Only PUSH:")
    ns.notify(
        [rachit.name, deepanshi.name],
        [ChannelTypes.PUSH],
        "Hello There")

    print("---------------------------------")

    print("All Channels:")
    ns.notify(
        [rachit.name, deepanshi.name],
        [ChannelTypes.SMS, ChannelTypes.PUSH, ChannelTypes.EMAIL],
        "Hello There")

    print("---------------------------------")
    print("End of test case")
    print("---------------------------------")

def test_unsubscribe():
    rachit = User("Rachit", "a@gmail.com", "123456", "apple_15")
    deepanshi = User("Deepanshi", "b@gmail.com", "234567", "pixel_9")

    ns = NotificationService()
    ns.register_user(rachit)
    ns.register_user(deepanshi)

    ns.subscribe_channel(rachit.name, ChannelTypes.SMS)
    ns.subscribe_channel(rachit.name, ChannelTypes.PUSH)

    ns.subscribe_channel(deepanshi.name, ChannelTypes.EMAIL)
    ns.subscribe_channel(deepanshi.name, ChannelTypes.PUSH)

    print("Only PUSH:")
    ns.notify(
        [rachit.name, deepanshi.name],
        [ChannelTypes.PUSH],
        "Hello There")

    print("---------------------------------")

    ns.unsubscribe_channel(rachit.name, ChannelTypes.PUSH)
    print("Only PUSH:")
    ns.notify(
        [rachit.name, deepanshi.name],
        [ChannelTypes.PUSH],
        "Hello There")

    print("---------------------------------")
    print ("End of test case")
    print("---------------------------------")

def test_deregister():
    rachit = User("Rachit", "a@gmail.com", "123456", "apple_15")
    deepanshi = User("Deepanshi", "b@gmail.com", "234567", "pixel_9")

    ns = NotificationService()
    ns.register_user(rachit)
    ns.register_user(deepanshi)

    ns.subscribe_channel(rachit.name, ChannelTypes.SMS)
    ns.subscribe_channel(rachit.name, ChannelTypes.PUSH)

    ns.subscribe_channel(deepanshi.name, ChannelTypes.EMAIL)
    ns.subscribe_channel(deepanshi.name, ChannelTypes.PUSH)
    try:
        print("Only PUSH:")
        ns.notify(
            [rachit.name, deepanshi.name],
            [ChannelTypes.PUSH],
            "Hello There")

        print("---------------------------------")

        ns.deregister_user(rachit.name)
        print("Only PUSH:")
        ns.notify(
            [rachit.name, deepanshi.name],
            [ChannelTypes.PUSH],
            "Hello There")
    except Exception as exp:
        print("Exception: {}. Traceback: {}".format(exp, traceback.format_exc()))

    print("---------------------------------")
    print ("End of test case")
    print("---------------------------------")

if __name__ == '__main__':
    # test_notifications()

    # test_unsubscribe()

    test_deregister()