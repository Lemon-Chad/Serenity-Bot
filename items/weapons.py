from objects.items import Weapon
from objects.stats import Stats

class StandardSword(Weapon):
    def __init__(self) -> None:
        super().__init__("Standard Sword", "+2 STR", "🗡️", Stats(strength=2))


class StandardDagger(Weapon):
    def __init__(self) -> None:
        super().__init__("Standard Dagger", "+1 STR +2 LCK", "🗡️", Stats(strength=1, luck=2))


class StandardShield(Weapon):
    def __init__(self) -> None:
        super().__init__("Standard Shield", "+1 DEF +1 LCK", "🛡️", Stats(defense=1, luck=1))


class StandardBow(Weapon):
    def __init__(self) -> None:
        super().__init__("Standard Bow", "+1 STR +1 SPD", "🏹", Stats(strength=1, speed=1))
