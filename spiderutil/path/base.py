from abc import abstractmethod

from ..typing import MediaType


class PathGenerator:

    def __init__(self, folder_path):
        folder_path = os.path.abspath(folder_path)
        self.check(folder_path)
        self.folder_path = folder_path

    @abstractmethod
    def path(self, **kwargs):
        pass

    @staticmethod
    def check(path):
        if not os.path.isdir(path):
            os.makedirs(path)

    @staticmethod
    def ext(media_type):
        return 'mp4' if media_type == MediaType.video else 'jpg'
