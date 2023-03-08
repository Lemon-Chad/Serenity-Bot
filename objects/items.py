from abc import ABC, abstractmethod


class ItemUseResponse():
    used: bool
    message: str
    
    def __init__(self, used: bool, message: str) -> None:
        self.used = used
        self.message = message
        
    def ok(message: str = None):
        return ItemUseResponse(True, message)

    def fail(message: str):
        return ItemUseResponse(False, message)


class Item(ABC):
    name: str
    description: str
    emoji: str
    
    def __init__(self, name: str, description: str, emoji: str) -> None:
        self.name = name
        self.description = description
        self.emoji = emoji
        
    @abstractmethod
    async def on_use(self, context) -> ItemUseResponse:
        return ItemUseResponse.fail("Undefined Item")
    

class HealthPotion(Item):
    def __init__(self) -> None:
        super().__init__("Health Potion", "Heals 2 HP", "🧪")
    
    async def on_use(self, context) -> ItemUseResponse:
        player = context.player
        if player.hp >= player.max_hp:
            return ItemUseResponse.fail("Player is already at Max HP!")
        player.hp = min(player.hp + 2, player.max_hp)
        return ItemUseResponse.ok()

