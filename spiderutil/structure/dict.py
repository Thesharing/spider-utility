class Dict:
    def __init__(self, structure=None, **kwargs):
        if type(structure) is dict:
            for k, v in kwargs:
                structure[k] = v
        self.__initial__ = structure

    def __new__(cls, structure=None, **kwargs):
        self = super(Dict, cls).__new__(cls)
        self.__init__(structure=structure, **kwargs)
        if type(self.__initial__) is dict:
            self.__dict__ = {key: Dict(self.__initial__[key]) for key in self.__initial__}
        elif type(self.__initial__) is list:
            self = [Dict(item) for item in self.__initial__]
        else:
            self = self.__initial__
        return self

    def __str__(self):
        return str(self.dict)

    @property
    def dict(self):
        return {k: v for k, v in self.__dict__.items() if k[0] != '_'}
