from .AbstractOutputHandler import AbstractOutputHandler

class ConsoleOPHandler(AbstractOutputHandler):
    def write(self, text):
        print(text)
