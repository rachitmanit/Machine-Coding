class User:
    def __init__(self, name, email, device_id, phone):
        self.name = name
        self.email = email
        self.device_id = device_id
        self.phone = phone

    def __str__(self):
        return f'Name: {self.name}, Email: {self.email}, Phone: {self.phone}, Device ID: {self.device_id}'