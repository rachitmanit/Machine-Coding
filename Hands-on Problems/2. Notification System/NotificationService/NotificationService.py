import threading
import importlib

from Channels.ChannelTypes import ChannelTypes
from Helper.Retry import ExponentialRetry
from Helper.Singleton import Singleton
from .Configuration import NotificationConfiguration

class NotificationService(metaclass=Singleton):

    def __init__(self):
        self.users = dict()
        self.config = NotificationConfiguration()
        self._lock = threading.Lock()
        self._user_locks = dict()
        self.channels = dict()
        self.load_channels()

    def load_channels(self):
        module = importlib.import_module("Channels.Channels")

        for channel in ChannelTypes:
            class_name = channel.name[0] + channel.name[1:].lower()
            channel_class = getattr(module, class_name)
            self.channels[channel] = channel_class()

    def register_user(self, user):
        with self._lock:
            self.users[user.name] = user
            self._user_locks[user.name] = threading.Lock()

    def validate_user(self, username):
        if username not in self.users:
            raise RuntimeError("User not registered")

    def subscribe_channel(self, username, channel):
        # print("Subscribing channel: {} for user: {}".format(channel, username))
        with self._user_locks[username]:
            self.validate_user(username)
            self.config.add_or_update_config(username, channel)

    def unsubscribe_channel(self, username, channel):
        with self._user_locks[username]:
            self.validate_user(username)
            self.config.remove_user_channel(username, channel)

    def deregister_user(self, username):
        with self._lock:
            self.config.remove_user_config(username)
            self.users.pop(username)

    def validate_notify(self, usernames, channels):
        if not isinstance(usernames, list):
            raise RuntimeError("usernames must be list")
        if not isinstance(channels, list):
            raise RuntimeError("channels must be list")

    def notify_user(self, user, channels, content):
        with self._user_locks[user]:
            user_channels = self.config.get_user_channels(user)
            for channel in channels:
                if channel in user_channels:
                    ExponentialRetry.exponential_retry(self.channels[channel].notify, args=(self.users[user], content))
                    # self.channels[channel].notify(self.users[user], content)

    def notify(self, usernames, channels, content):
        self.validate_notify(usernames, channels)
        for user in usernames:
            self.notify_user(user, channels, content)

