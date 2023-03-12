import pickle
import os


if os.path.exists("storage.dat"):
    with open("storage.dat", "rb") as f:
        _data = pickle.load(f)
else:
    _data = {
        "accounts": {},
        "lost_gear": []
    }


def get_account(user_id: int):
    return _data[user_id]


def find_lost_gear(user_id: int):
    applicable = [ x for x in _data["lost_gear"] if x.lost_owner != user_id ]
    if not applicable:
        return None
    return applicable[0]


def add_lost_gear(item):
    _data["lost_gear"].append(item)


def create_account(user_id: int, acc):
    _data[user_id] = acc


def save_data():
    with open("storage.dat", "wb+") as f:
        pickle.dump(_data, f)
