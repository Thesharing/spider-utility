import os
import re
from abc import abstractmethod
from typing import Union

from ..typing import MediaType
from ..exceptions import NullValueException

convert_to_ext = {
    'video': 'mp4',
    MediaType.video: 'mp4',
    'image': 'jpg',
    MediaType.image: 'jpg'
}


class PathGenerator:

    def __init__(self, folder_path):
        folder_path = os.path.abspath(folder_path)
        self.check(folder_path)
        self.folder_path = folder_path

    @abstractmethod
    def generate(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def direct(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def check(path):
        if not os.path.isdir(path):
            os.makedirs(path)

    @staticmethod
    def ext(media_type: Union[str, MediaType]):
        return convert_to_ext[media_type]

    def join(self, file_name):
        file_name = re.sub(r'[\\/:"*?<>|]+', '', file_name)
        if len(file_name) > 0:
            return os.path.join(self.folder_path, file_name)
        else:
            raise NullValueException('Null file name.')
