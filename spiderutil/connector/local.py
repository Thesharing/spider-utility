import os

from .base import Database


class LocalFile(Database):
    def __init__(self, file_path: str, file_type=None):
        super(LocalFile, self).__init__(os.path.basename(file_path), 'LocalFile')
        self.file_path = file_path
        self.file_type = file_type

    def count(self):
        if os.path.isdir(self.file_path):
            if self.file_type:
                return len([name for name in os.listdir(self.file_path) if
                            os.path.isfile(os.path.join(self.file_path, name)) and os.path.splitext(
                                name) == self.file_type])
            else:
                return len([name for name in os.listdir(self.file_path)
                            if os.path.isfile(os.path.join(self.file_path, name))])
        else:
            return 0
