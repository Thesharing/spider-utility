from .base import PathGenerator


class StoreSimply(PathGenerator):

    def path(self, media_type, file_name, **kwargs):
        return os.path.join(self.folder_path, '{0}.{1}'.format(file_name, self.ext(media_type)))
