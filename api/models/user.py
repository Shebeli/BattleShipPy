from api.models.base import AbstractCustomSet


class User:
    def __init__(self, id_, username):
        self.id = id_
        self.username = username

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def __str__(self):
        return f"Username: {self.username}| id: {self.id}"


class UserSet(AbstractCustomSet):
    sub_class = User
