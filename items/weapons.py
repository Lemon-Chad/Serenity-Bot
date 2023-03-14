from objects.items import ForgedWeapon, Weapon
from objects.stats import Stats

class StandardSword(Weapon):
    def __init__(self) -> None:
        super().__init__("Standard Sword", "+2 STR", "🗡️", Stats(strength=2))
        
    def forge(self, forge_level: int) -> ForgedWeapon:
        return ForgedSword(forge_level)


class StandardDagger(Weapon):
    def __init__(self) -> None:
        super().__init__("Standard Dagger", "+1 STR +2 LCK", "🗡️", Stats(strength=1, luck=2))
        
    def forge(self, forge_level: int) -> ForgedWeapon:
        return ForgedDagger(forge_level)


class StandardShield(Weapon):
    def __init__(self) -> None:
        super().__init__("Standard Shield", "+1 DEF +1 LCK", "🛡️", Stats(defense=1, luck=1))
        
    def forge(self, forge_level: int) -> ForgedWeapon:
        return ForgedShield(forge_level)


class StandardBow(Weapon):
    def __init__(self) -> None:
        super().__init__("Standard Bow", "+1 STR +1 SPD", "🏹", Stats(strength=1, speed=1))
        
    def forge(self, forge_level: int) -> ForgedWeapon:
        return ForgedBow(forge_level)


# FORGED WEAPONS


class ForgedSword(ForgedWeapon):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Sword", "🗡️", Stats(strength=2), forge_level)


class ForgedDagger(ForgedWeapon):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Dagger", "🗡️", Stats(strength=1, luck=2), forge_level)


class ForgedShield(ForgedWeapon):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Shield", "🛡️", Stats(defense=1, luck=1), forge_level)


class ForgedBow(ForgedWeapon):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Bow", "🏹", Stats(strength=1, speed=1), forge_level)

