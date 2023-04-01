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
    
    # TODO: Remove OP starter stash.
    def __init__(self, user: nextcord.User) -> None:
        self.user = user.id
        
        self.stash = Storage("Stash", 50)
        
        self.stash.insert_item(trinkets.AncientCoin())
        
        for _ in range(2):
            for _ in range(2):
                self.stash.insert_item(alloys.BronzeAlloy())
                self.stash.insert_item(alloys.CrystalAlloy())
                self.stash.insert_item(alloys.ExoticAlloy())
                self.stash.insert_item(alloys.IronAlloy())
                self.stash.insert_item(alloys.MysticAlloy())
                self.stash.insert_item(alloys.PlatinumAlloy())
                self.stash.insert_item(alloys.SteelAlloy())
                self.stash.insert_item(alloys.TitaniumAlloy())
            
            self.stash.insert_item(weapons.StandardBow())
            self.stash.insert_item(weapons.StandardSword())
            self.stash.insert_item(weapons.StandardDagger())
            self.stash.insert_item(weapons.StandardShield())
        
            self.stash.insert_item(armors.StandardHeadband())
            self.stash.insert_item(armors.StandardSkates())
            self.stash.insert_item(armors.StandardHelmet())
            self.stash.insert_item(armors.StandardRobe())
            self.stash.insert_item(armors.StandardScarf())
            self.stash.insert_item(armors.StandardShoes())
            self.stash.insert_item(armors.StandardSkull())
            self.stash.insert_item(armors.StandardTunic())
        
        self.player = DisCharacter(10, 0, 0, 0, 5, self.user)
        
        self.money = 1_000_000
        
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
