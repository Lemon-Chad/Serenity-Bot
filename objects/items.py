from abc import ABC, abstractmethod
from typing import Tuple
from objects.stats import Stats
from objects.slots import EquipSlots
from typing import List


class ItemType:
    GENERIC = 0
    CONSUMABLE = 1
    WEAPON = 2
    ARMOR = 3


class ItemUseResponse():
    used: bool
    message: str
    
    def __init__(self, used: bool, message: str) -> None:
        self.used = used
        self.message = message
        
    def ok(message: str):
        return ItemUseResponse(True, message)

    def fail(message: str):
        return ItemUseResponse(False, message)


class Item(ABC):
    name: str
    description: str
    emoji: str
    item_type: int
    value: int
    slot: List[bool]
    lost_owner: int
    forged: bool
    
    def __init__(self, name: str, description: str, emoji: str, item_type: int, value: int) -> None:
        self.name = name
        self.description = description
        self.emoji = emoji
        self.item_type = item_type
        self.value = value
        self.slot = [False, False, False, False]
        self.lost_owner = None
        self.forged = False
        
    @abstractmethod
    async def on_use(self, context) -> ItemUseResponse:
        return ItemUseResponse.fail("Undefined Item")


class GenericItem(Item):
    def __init__(self, name: str, description: str, emoji: str, value: int) -> None:
        super().__init__(name, description, emoji, ItemType.GENERIC, value)
    
    async def on_use(self, _) -> ItemUseResponse:
        return ItemUseResponse.fail("Generic Item Use")


class ForgePerkMaterialItem(GenericItem):
    bonus: Stats
    
    def __init__(self, name: str, description: str, emoji: str, value: int, bonus: Stats) -> None:
        super().__init__(name, description, emoji, value)
        self.bonus = bonus


class ForgeMaterialItem(GenericItem):
    forge_level: int
    
    def __init__(self, name: str, description: str, emoji: str, value: int, forge_level: int) -> None:
        super().__init__(name, description, emoji, value)
        self.forge_level = forge_level


class ForgedItem(Item):
    stats: Stats
    forge_level: int
    
    def __init__(self, name: str, emoji: str, item_type: int, value: int, base_stats: Stats, forge_level: int) -> None:
        self.stats = Stats(*[ forged_stat(x, forge_level) for x in base_stats ])
        self.forge_level = forge_level
        
        super().__init__(
            name, 
            " ".join([
                "+" + str(x) + " " + STAT_KEY[i]
                for i, x in enumerate(self.stats)
                if x > 0
            ]), 
            emoji, 
            item_type, 
            value * (3 * forge_level + 1)
        )
        
    def add_bonus(self, bonus: Stats):
        self.stats += bonus
        self.description = " ".join([
            "+" + str(x) + " " + STAT_KEY[i]
            for i, x in enumerate(self.stats)
            if x > 0
        ])

    async def on_use(self, _) -> ItemUseResponse:
        return ItemUseResponse.fail("Forged Type Item")


class ForgeableItem(Item):
    def __init__(self, name: str, description: str, emoji: str, item_type: int, value: int) -> None:
        super().__init__(name, description, emoji, item_type, value)
        
    @abstractmethod
    def forge(self, forge_level: int) -> ForgedItem:
        return None


class Weapon(ForgeableItem):
    stats: Stats
    
    def __init__(self, name: str, description: str, emoji: str, stats: Stats) -> None:
        super().__init__(name, description, emoji, ItemType.WEAPON, 2)
        self.stats = stats
        
        self.slot[EquipSlots.MAINHAND] = True
        self.slot[EquipSlots.OFFHAND] = True

    async def on_use(self, _) -> ItemUseResponse:
        return ItemUseResponse.fail("Weapon Type Item")


class ConsumableItem(Item):
    def __init__(self, name: str, description: str, emoji: str) -> None:
        super().__init__(name, description, emoji, ItemType.CONSUMABLE, 3)


class Helmet(ForgeableItem):
    stats: Stats
    
    def __init__(self, name: str, description: str, emoji: str, stats: Stats) -> None:
        super().__init__(name, description, emoji, ItemType.ARMOR, 2)
        self.stats = stats
        
        self.slot[EquipSlots.HELMET] = True

    async def on_use(self, _) -> ItemUseResponse:
        return ItemUseResponse.fail("Armor Type Item")


class Armor(ForgeableItem):
    stats: Stats
    
    def __init__(self, name: str, description: str, emoji: str, stats: Stats) -> None:
        super().__init__(name, description, emoji, ItemType.ARMOR, 3)
        self.stats = stats
        
        self.slot[EquipSlots.ARMOR] = True

    async def on_use(self, _) -> ItemUseResponse:
        return ItemUseResponse.fail("Armor Type Item")


def forged_stat(x, lvl):
    return round(x * (1 + lvl / 2))


STAT_KEY = [
    "HP",
    "DEF",
    "STR",
    "SPD",
    "LCK"
]


class ForgedWeapon(ForgedItem):
    def __init__(self, name: str, emoji: str, base_stats: Stats, forge_level: int) -> None:
        super().__init__(name, emoji, ItemType.WEAPON, 2, base_stats, forge_level)
        
        self.slot[EquipSlots.MAINHAND] = True
        self.slot[EquipSlots.OFFHAND] = True


class ForgedHelmetItem(ForgedItem):
    def __init__(self, name: str, emoji: str, base_stats: Stats, forge_level: int) -> None:
        super().__init__(name, emoji, ItemType.WEAPON, 2, base_stats, forge_level)
        
        self.slot[EquipSlots.HELMET] = True


class ForgedArmorItem(ForgedItem):
    def __init__(self, name: str, emoji: str, base_stats: Stats, forge_level: int) -> None:
        super().__init__(name, emoji, ItemType.WEAPON, 3, base_stats, forge_level)
        
        self.slot[EquipSlots.ARMOR] = True



