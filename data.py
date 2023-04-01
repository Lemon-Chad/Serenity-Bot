import pickle
import os


def wipe_data():
    _data["accounts"] = {}
    _data["lost_gear"] = []


if os.path.exists("storage.dat"):
    with open("storage.dat", "rb") as f:
        _data = pickle.load(f)
else:
    _data = {}
    wipe_data()


def top_accounts():
    return sorted(_data["accounts"].values(), key=lambda x: x.money, reverse=True)


def has_account(user_id: int):
    return user_id in _data["accounts"]


def get_account(user_id: int):
    return _data["accounts"][user_id]


def find_lost_gear(user_id: int, min_level: int, max_level: int):
    applicable = [ x for x in _data["lost_gear"] if x.lost_owner != user_id and min_level <= x.forge_level <= max_level ]
    if not applicable:
        return None
    i = applicable[0]
    _data["lost_gear"].remove(i)
    return i


def add_lost_gear(item):
    _data["lost_gear"].append(item)


def create_account(user_id: int, acc):
    _data["accounts"][user_id] = acc


def save_data():
    for acc in _data["accounts"].values():
        acc.in_dungeon = False
        acc.close_menu()
    print(_data)
    with open("storage.dat", "wb+") as f:
        pickle.dump(_data, f)


if __name__ == "__main__":
    save_data()
