from enum import Enum


class MediaType(Enum):
    """
    Enumeration of medias, at present the type is categorized as `video`, `photo` and `other`.
    """
    video = 1
    photo = 2
    other = 3

    @staticmethod
    def convert(name: str):
        """
        Convert enumeration name to enumeration MediaType
        :param name: str, name of MediaType
        :return: enumeration MediaType
        """
        return MediaType(name.lower())
