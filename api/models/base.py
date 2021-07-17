from itertools import count


class CustomSet(set):
    """A custom set for creating objects with a counter for each object id and some extra methods"""
    sub_class = None

    def __init__(self, iterable=[]):
        self._counter = count(1)
        super().__init__(iterable)

    @property
    def ids(self):
        return [obj.id for obj in self]

    def create_and_add(self, val):
        obj = self.sub_class(next(self._counter), val)
        self.add(obj)
        return obj

    def get(self, id):
        for obj in self:
            if obj.id == id:
                return obj
        return

    def remove_id(self, id):
        obj = self.get(id)
        if not obj:
            raise Exception("No object with given id exists in this set")
        self.remove(obj)
