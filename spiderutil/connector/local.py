import os
import json

from .base import Database


class LocalFolder(Database):
    """
    Support counting the files and creating new files.
    """

    def __init__(self, folder_path: str, file_ext=None):
        """
        :param folder_path: the folder path, support relative path and absolute path
        :param file_ext: the extension suffix used to filter the files, default is ``None``
        """
        super(LocalFolder, self).__init__(os.path.basename(folder_path),
                                          'LocalFolder')
        self.folder_path = os.path.abspath(folder_path)
        if file_ext[0] == '.':
            file_ext = file_ext[1:]
        self.file_ext = file_ext

    @staticmethod
    def _ext(name):
        if len(name) > 0:
            file_name, ext = os.path.splitext(name)
            return ext[1:] if len(ext) > 0 else file_name

    @property
    def exists(self):
        """
        Check if the folder exists or not
        """
        return os.path.isdir(self.folder_path)

    def list(self, include_folder=False):
        """
        Return the file list filtered by:

        1. if ``file_ext`` specified, the list only contains file with specified extension suffix
        2. if ``include_folder`` is True, the list also contains folders

        :param include_folder: include folders or not, default is ``False``
        :return: Generator of the filtered file list.
        """

        def condition(name):
            path = os.path.join(self.folder_path, name)
            return (include_folder or os.path.isfile(path)) and (not self.file_ext or self._ext(name) == self.file_ext)

        return filter(lambda name: condition(name), os.listdir(self.folder_path))

    def count(self, include_folder=False):
        if self.exists:
            return len([self.list(include_folder)])
        else:
            raise FileNotFoundError('Folder {} not exists'.format(self.folder_path))

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
