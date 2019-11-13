import json

from io import IOBase


class Dict(dict):
    def __init__(self, source=None, **kwargs):
        super(Dict, self).__init__()
        for k, v in kwargs.items():
            if k not in self:
                self[k] = v

    def __new__(cls, source=None, **kwargs):
        self = super(Dict, cls).__new__(cls)
        self.__init__(source=source, **kwargs)
        if isinstance(source, dict):
            for k, v in source.items():
                self[k] = Dict(v)
        elif isinstance(source, list):
            self = [Dict(item) for item in source]
        else:
            self = source
        return self

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError("The dict has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value


class TextDict(dict):

    @staticmethod
    def load(source):
        if isinstance(source, IOBase):
            return json.load(source, object_hook=lambda pairs: TextDict(pairs.items()))
        elif isinstance(source, str):
            return json.loads(source, object_hook=lambda pairs: TextDict(pairs.items()))

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError("The dict has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value
