import nextcord
from objects.entities import DisCharacter
from objects.storage import Storage


class Account:
    player: DisCharacter
    user: int
    stash: Storage
    money: int
    in_dungeon: bool
    
    def __init__(self, user: nextcord.User) -> None:
        self.user = user.id
        
        self.stash = Storage("Stash", 50)
        self.player = DisCharacter(10, 0, 0, 0, 5, self.user)
        
        self.money = 0
        self.in_dungeon = False
        
