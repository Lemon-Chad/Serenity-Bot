import pickle
import os


if os.path.exists("storage.dat"):
    with open("storage.dat", "rb") as f:
        _data = pickle.load(f)
else:
    _data = {
        "accounts": {}
    }


def get_account(user_id: int):
    return _data[user_id]


def create_account(user_id: int, acc):
    _data[user_id] = acc


def save_data():
    with open("storage.dat", "wb+") as f:
        pickle.dump(_data, f)
