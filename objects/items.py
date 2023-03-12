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


class Weapon(Item):
    stats: Stats
    
    def __init__(self, name: str, description: str, emoji: str, stats: Stats) -> None:
        super().__init__(name, description, emoji, ItemType.WEAPON, 2)
        self.stats = stats
        
        self.slot[EquipSlots.MAINHAND] = True
        self.slot[EquipSlots.OFFHAND] = True

    async def on_use(self, _) -> ItemUseResponse:
        return ItemUseResponse.fail("Weapon Type Item")


class Consumable(Item):
    def __init__(self, name: str, description: str, emoji: str) -> None:
        super().__init__(name, description, emoji, ItemType.CONSUMABLE, 3)


class Helmet(Item):
    stats: Stats
    
    def __init__(self, name: str, description: str, emoji: str, stats: Stats) -> None:
        super().__init__(name, description, emoji, ItemType.ARMOR, 2)
        self.stats = stats
        
        self.slot[EquipSlots.HELMET] = True

    async def on_use(self, _) -> ItemUseResponse:
        return ItemUseResponse.fail("Armor Type Item")


class Armor(Item):
    stats: Stats
    
    def __init__(self, name: str, description: str, emoji: str, stats: Stats) -> None:
        super().__init__(name, description, emoji, ItemType.ARMOR, 3)
        self.stats = stats
        
        self.slot[EquipSlots.ARMOR] = True

    async def on_use(self, _) -> ItemUseResponse:
        return ItemUseResponse.fail("Armor Type Item")

