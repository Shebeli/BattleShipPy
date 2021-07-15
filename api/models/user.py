from itertools import count


class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username


class UserSet:
    def __init__(self):
        self.counter = count(1)
        self.users = set()

    @property
    def users_id(self):
        return [user.id for user in self.users]

    def get(self, id):
        for user in self.users:
            if user.id == id:
                return user
        return

    def create_and_add(self, username):
        user = User(next(self.counter), username)
        self.users.add(user)
        return user

    def remove(self, id):
        user = self.get(id)
        if not user:
            raise Exception("Given user id does not exist")
        self.users.remove(user)