from objects.items import ConsumableItem, ItemUseResponse
import objects.context as rpgctx

class HealthPotion(ConsumableItem):
    def __init__(self) -> None:
        super().__init__("Health Potion I", "Heals 2 HP", "🧪")
    
    async def on_use(self, context) -> ItemUseResponse:
        player = context.player
        if player.hp >= player.max_hp:
            return ItemUseResponse.fail("Player is already at Max HP")
        player.heal(2)
        return ItemUseResponse.ok("Healed 2 HP")


class HealthPotionII(ConsumableItem):
    def __init__(self) -> None:
        super().__init__("Health Potion II", "Heals 5 HP", "🧪")
    
    async def on_use(self, context) -> ItemUseResponse:
        player = context.player
        if player.hp >= player.max_hp:
            return ItemUseResponse.fail("Player is already at Max HP")
        player.heal(5)
        return ItemUseResponse.ok("Healed 5 HP")


class HealthPotionIII(ConsumableItem):
    def __init__(self) -> None:
        super().__init__("Health Potion III", "Heals 15 HP", "🧪")
    
    async def on_use(self, context) -> ItemUseResponse:
        player = context.player
        if player.hp >= player.max_hp:
            return ItemUseResponse.fail("Player is already at Max HP")
        player.heal(15)
        return ItemUseResponse.ok("Healed 15 HP")


class Grenade(ConsumableItem):
    def __init__(self) -> None:
        super().__init__("Grenade I", "Deals 5 DMG", "🧨")
    
    async def on_use(self, context: rpgctx.BattleContext) -> ItemUseResponse:
        if not isinstance(context, rpgctx.BattleContext):
            return ItemUseResponse.fail("Must be used in battle")
        enemy = context.enemy
        return ItemUseResponse.ok(f"Dealt {enemy.damage(5)} DMG")


class GrenadeII(ConsumableItem):
    def __init__(self) -> None:
        super().__init__("Grenade II", "Deals 10 DMG", "🧨")
    
    async def on_use(self, context: rpgctx.BattleContext) -> ItemUseResponse:
        if not isinstance(context, rpgctx.BattleContext):
            return ItemUseResponse.fail("Must be used in battle")
        enemy = context.enemy
        return ItemUseResponse.ok(f"Dealt {enemy.damage(10)} DMG")


class GrenadeIII(ConsumableItem):
    def __init__(self) -> None:
        super().__init__("Grenade III", "Deals 15 DMG", "🧨")
    
    async def on_use(self, context: rpgctx.BattleContext) -> ItemUseResponse:
        if not isinstance(context, rpgctx.BattleContext):
            return ItemUseResponse.fail("Must be used in battle")
        enemy = context.enemy
        return ItemUseResponse.ok(f"Dealt {enemy.damage(15)} DMG")
