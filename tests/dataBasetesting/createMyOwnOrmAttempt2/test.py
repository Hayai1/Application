class Table:
    @classmethod
    def _hello(cls):
        return cls

class Author(Table):
    pass



assert Author._hello() == Author
