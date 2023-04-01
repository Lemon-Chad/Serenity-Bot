import nextcord
from nextcord.ui import View
from objects.entities import DisCharacter
from objects.storage import Storage
from items import alloys, weapons, armors, trinkets


class Account:
    player: DisCharacter
    user: int
    stash: Storage
    money: int
    in_dungeon: bool
    in_menu: bool
    menu: View
    
    def __init__(self, user: nextcord.User) -> None:
        self.user = user.id
        
        self.stash = Storage("Stash", 50)
        
        self.player = DisCharacter(10, 0, 0, 0, 5, self.user, user.name)
        
        self.money = 0
        
        self.in_dungeon = False
        self.in_menu = False
        self.menu = None
    
    def open_menu(self, v: View):
        self.menu = v
        return v
    
    def close_menu(self):
        self.in_menu = False
        if self.menu is not None:
            self.menu.stop()
            self.menu = None
