import re
import os
from typing import Union

from .base import PathGenerator
from ..typing import MediaType


class StoreByUserName(PathGenerator):

    def __init__(self, folder_path: str):
        PathGenerator.__init__(self, folder_path)
        self.users = {}
        self._init_all_users()

    def generate(self, user_name: str, media_type: Union[str, MediaType],
                 **kwargs):
        if user_name not in self.users:
            # If not appeared before
            self.users[user_name] = 1
        count = self.users[user_name]
        # The count is always the index of next media file
        self.users[user_name] += 1
        return self.join(
            '{0}-{1}.{2}'.format(user_name, count, self.ext(media_type)))

    def direct(self, file_name: str, media_type: Union[str, MediaType] = None,
               **kwargs):
        if media_type:
            return self.join('{0}.{1}'.format(file_name, self.ext(media_type)))
        else:
            return self.join(file_name)

    def _init_all_users(self):
        # Traverse all the files, the file name should be '[Username]-[Index].[Ext]]'
        for file_name in os.listdir(self.folder_path):
            match = re.search(r'(.+)-(\d+)(?!.+)',
                              os.path.splitext(file_name)[0])
            if match is not None:
                user_name = match.group(1)
                count = int(match.group(2))
                self.users[user_name] = max(self.users[user_name], count + 1) \
                    if user_name in self.users else count + 1


class StoreByUserNamePerFolder(PathGenerator):

    def __init__(self, folder_path: str):
        PathGenerator.__init__(self, folder_path)
        self.users = {}

    def generate(self, user_name: str, media_type: Union[str, MediaType],
                 **kwargs):
        # Check if the folder named by username exists
        self.check(os.path.join(self.folder_path, user_name))
        if user_name not in self.users:
            self._init_user(user_name)
        count = self.users[user_name]
        self.users[user_name] += 1
        return self.join(os.path.join(user_name,
                                      '{1}.{2}'.format(user_name, count,
                                                       self.ext(media_type))))

    def direct(self, file_name: str, media_type: Union[str, MediaType] = None,
               **kwargs):
        if media_type:
            return self.join(file_name)
        else:
            return self.join('{0}.{1}'.format(file_name, self.ext(media_type)))

    def _init_user(self, user_name: str):
        # Traverse the sub folder of specific user, the file name should be '[Username]/[Index].[Ext]'
        path = self.join(user_name)
        count = 0
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                match = re.search(r'\d+', os.path.splitext(file_name)[0])
                if match is not None:
                    self.users[user_name] = max(count, int(match.group(0)))
        self.users[user_name] = count + 1
