from .AbstractOutputHandler import AbstractOutputHandler

class FileOPHandler(AbstractOutputHandler):

    def __init__(self, file_name):
        self.file_name = file_name
        self._filehandler = open(self.file_name, 'a+')

    def write(self, text):
        self._filehandler.writelines(text + "\n")

    def close(self):
        self._filehandler.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()