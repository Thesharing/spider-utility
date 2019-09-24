class Dict:
    def __init__(self, structure=None, **kwargs):
        if type(structure) is dict:
            for k, v in kwargs:
                structure[k] = v
        self.dict = structure

    def __new__(cls, structure=None, **kwargs):
        self = super(Dict, cls).__new__(cls)
        self.__init__(structure=structure, **kwargs)
        if type(self.dict) is dict:
            self.__dict__ = {key: Dict(self.dict[key]) for key in self.dict}
        elif type(self.dict) is list:
            self = [Dict(item) for item in self.dict]
        else:
            self = self.dict
        return self

    def __str__(self):
        return str(self.dict)
