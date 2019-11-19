import os
import json

from .base import Database


class LocalFolder(Database):
    def __init__(self, folder_path: str, file_type=None):
        super(LocalFolder, self).__init__(os.path.basename(folder_path),
                                          'LocalFolder')
        self.folder_path = folder_path
        self.file_type = file_type

    def count(self):
        if os.path.isdir(self.folder_path):
            if self.file_type:
                return len([name for name in os.listdir(self.folder_path) if
                            os.path.isfile(os.path.join(self.folder_path, name))
                            and os.path.splitext(name) == self.file_type])
            else:
                return len([name for name in os.listdir(self.folder_path)
                            if os.path.isfile(os.path.join(self.folder_path,
                                                           name))])
        else:
            return 0

    def add(self, item):
        if not os.path.isfile(item):
            with open(item, 'wb'):
                pass

    def __contains__(self, item):
        return os.path.isfile(os.path.join(self.folder_path, item))


class LocalFile(Database):
    def __init__(self, file_path: str, encoding='utf-8'):
        super(LocalFile, self).__init__(os.path.basename(file_path),
                                        'LocalFile')
        self.file_path = file_path
        self.data = None
        self.encoding = encoding
        with open(self.file_path, 'r', encoding=encoding) as f:
            self.data = json.load(f)

    def count(self):
        return len(self.data)

    def add(self, item):
        self.data.append(item)
        self.save()

    def save(self):
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            json.dump(self.data, f)

    def __contains__(self, item):
        return item in self.data
