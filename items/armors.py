from objects.items import Helmet, Armor
from objects.stats import Stats

class StandardHelmet(Helmet):
    def __init__(self) -> None:
        super().__init__("Standard Helmet", "+2 DEF", "🪖", Stats(defense=2))


class StandardHeadband(Helmet):
    def __init__(self) -> None:
        super().__init__("Standard Headband", "+1 DEF +2 LCK", "🧣", Stats(defense=1, luck=2))


class StandardScarf(Helmet):
    def __init__(self) -> None:
        super().__init__("Standard Headband", "+4 LCK", "🧣", Stats(defense=1, luck=4))


class StandardSkull(Helmet):
    def __init__(self) -> None:
        super().__init__("Standard Skull", "+1 STR +1 DEF", "💀", Stats(strength=1, defense=1))


class StandardTunic(Armor):
    def __init__(self) -> None:
        super().__init__("Standard Tunic", "+2 DEF", "🦺", Stats(defense=2))


class StandardRobe(Armor):
    def __init__(self) -> None:
        super().__init__("Standard Robe", "+1 DEF +1 SPD", "🥋", Stats(defense=1, speed=1))


class StandardShoes(Armor):
    def __init__(self) -> None:
        super().__init__("Standard Shoes", "+1 SPD +1 LCK", "👟", Stats(luck=1, speed=1))


class StandardSkates(Armor):
    def __init__(self) -> None:
        super().__init__("Standard Skates", "+2 SPD", "🛼", Stats(speed=2))
