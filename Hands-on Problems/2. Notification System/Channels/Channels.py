from Channels.AbstractChannel import AbstractChannel


class Email(AbstractChannel):

    def notify(self, user, content):
        print("Sent Email to user: {} at email: {}. Content: {}".format(user.name, user.email, content))


class Sms(AbstractChannel):
    def notify(self, user, content):
        print("Sent SMS to user: {} at phone: {}. Content: {}".format(user.name, user.phone, content))


class Push(AbstractChannel):
    def notify(self, user, content):
        print("Sent Push to user: {} at device_id: {}. Content: {}".format(user.name, user.device_id, content))
