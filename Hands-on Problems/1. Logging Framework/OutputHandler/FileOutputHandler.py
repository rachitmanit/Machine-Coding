from .AbstractOutputHandler import AbstractOutputHandler

class FileOPHandler(AbstractOutputHandler):

    def __init__(self, file_name):
        self.file_name = file_name
        try:
            self._filehandler = open(self.file_name, 'a+')
        except Exception as exp:
            print("Error opening file {} by FileOPHandler".format(self.file_name))
            self._filehandler = None

    def write(self, text):
        try:
            if self.file_name:
                self._filehandler.writelines(text + "\n")
        except Exception as exp:
            print("Failed to write message in file {}".format(self.file_name))

    def close(self):
        if self._filehandler:
            self._filehandler.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()