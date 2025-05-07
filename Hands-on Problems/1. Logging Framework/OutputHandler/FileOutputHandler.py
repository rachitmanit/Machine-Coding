import datetime
import os.path
import time

from .AbstractOutputHandler import AbstractOutputHandler

class FileOPHandler(AbstractOutputHandler):

    def __init__(self, file_name, threshold=10240, rotation_check_interval=5):
        self.file_name = file_name
        self.threshold = threshold
        self.rotation_check_interval = rotation_check_interval
        self.last_check_time = time.time()
        try:
            self._filehandler = open(self.file_name, 'a+')
        except Exception as exp:
            print("Error opening file {} by FileOPHandler. Exception: {}".format(self.file_name, exp))
            self._filehandler = None

    def write(self, text):
        try:
            if self._filehandler:
                self._filehandler.writelines(text + "\n")
        except Exception as exp:
            print("Failed to write message in file {}".format(self.file_name))
            print(f'Outputting to Console Log: {text}')

        if time.time() - self.last_check_time > self.rotation_check_interval:
            self.log_rotate()
            self.last_check_time = time.time()

    def log_rotate(self):
        if os.path.exists(self.file_name) and os.path.getsize(self.file_name) / 1024 > self.threshold:
            if self._filehandler:
                self._filehandler.close()

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            rotated_file_name = self.file_name + f'_{timestamp}'

            try:
                os.rename(self.file_name, rotated_file_name)
                print(f'Rotated {self.file_name} to {rotated_file_name}')
                self._filehandler = open(self.file_name, 'a+')
            except Exception as exp:
                print(f'Failed to open file {self.file_name} by FileIOHandler. Exception: {exp}')
                self._filehandler = None


    def close(self):
        if self._filehandler:
            self._filehandler.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()