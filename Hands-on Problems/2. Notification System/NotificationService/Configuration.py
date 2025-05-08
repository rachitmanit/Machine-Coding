from Channels.ChannelTypes import ChannelTypes

class NotificationConfiguration:
    def __init__(self):
        self.config = dict()

    def validate_channel(self, channel):
        if channel not in ChannelTypes:
            raise RuntimeError("channel : {} is not supported".format(channel))

    def validate_user(self, username):
        if username not in self.config:
            raise RuntimeError("User: {} not present in config".format(username))

    def add_or_update_config(self, username, channel):
        self.validate_channel(channel)

        if username not in self.config:
            self.config[username] = list()

        if channel not in self.config[username]:
            self.config[username].append(channel)

    def remove_user_channel(self, username, channel):
        self.validate_user(username)
        self.validate_channel(channel)

        if channel in self.config[username]:
            self.config[username].remove(channel)

    def remove_user_config(self, username):
        self.validate_user(username)
        self.config.pop(username)

    def get_user_channels(self, username):
        self.validate_user(username)
        return self.config[username]
