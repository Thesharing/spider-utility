from typing import Union

from .base import PathGenerator
from ..typing import MediaType


class StoreSimply(PathGenerator):

    def generate(self, file_name: str, media_type: Union[str, MediaType], **kwargs):
        return self.join('{0}.{1}'.format(file_name, self.ext(media_type)))

    def direct(self, file_name: str, media_type: Union[str, MediaType] = None, **kwargs):
        if media_type:
            return self.generate(file_name, media_type)
        else:
            return self.join(file_name)
