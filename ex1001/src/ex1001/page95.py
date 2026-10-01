from typing import TypedDict

class User(TypedDict):
    id: int
    name: str
    email: str

def page95_user():
    user1: User = {
        'id': 1,
        'name': 'nayeon_park',
        'email': 'example@gmail.com'
    }
    print(user1)
    return user1
