import nextcord
from objects.entities import DisCharacter
from data import create_account
from objects.storage import Storage


class Account:
    player: DisCharacter
    user: nextcord.User
    stash: Storage
    money: int
    
    def __init__(self, user: nextcord.User) -> None:
        self.user = user
        create_account(self.user.id, self)
        
        self.stash = Storage("Stash", 50)
        self.player = DisCharacter(10, 0, 0, 0, 5, self.user)
        
        self.money = 0
        
