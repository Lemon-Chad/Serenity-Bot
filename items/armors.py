from objects.items import Helmet, Armor, ForgedHelmetItem, ForgedArmorItem
from objects.stats import Stats

class StandardHelmet(Helmet):
    def __init__(self) -> None:
        super().__init__("Standard Helmet", "+2 DEF", "🪖", Stats(defense=2))
        
    def forge(self, forge_level: int) -> ForgedHelmetItem:
        return ForgedHelmet(forge_level)


class StandardHeadband(Helmet):
    def __init__(self) -> None:
        super().__init__("Standard Headband", "+1 DEF +2 LCK", "🧣", Stats(defense=1, luck=2))
        
    def forge(self, forge_level: int) -> ForgedHelmetItem:
        return ForgedHeadband(forge_level)


class StandardScarf(Helmet):
    def __init__(self) -> None:
        super().__init__("Standard Headband", "+4 LCK", "🧣", Stats(defense=1, luck=4))
        
    def forge(self, forge_level: int) -> ForgedHelmetItem:
        return ForgedScarf(forge_level)


class StandardSkull(Helmet):
    def __init__(self) -> None:
        super().__init__("Standard Skull", "+1 STR +1 DEF", "💀", Stats(strength=1, defense=1))
        
    def forge(self, forge_level: int) -> ForgedHelmetItem:
        return ForgedSkull(forge_level)


class StandardTunic(Armor):
    def __init__(self) -> None:
        super().__init__("Standard Tunic", "+2 DEF", "🦺", Stats(defense=2))
        
    def forge(self, forge_level: int) -> ForgedArmorItem:
        return ForgedTunic(forge_level)


class StandardRobe(Armor):
    def __init__(self) -> None:
        super().__init__("Standard Robe", "+1 DEF +1 SPD", "🥋", Stats(defense=1, speed=1))
        
    def forge(self, forge_level: int) -> ForgedArmorItem:
        return ForgedRobe(forge_level)


class StandardShoes(Armor):
    def __init__(self) -> None:
        super().__init__("Standard Shoes", "+1 SPD +1 LCK", "👟", Stats(luck=1, speed=1))
        
    def forge(self, forge_level: int) -> ForgedArmorItem:
        return ForgedShoes(forge_level)


class StandardSkates(Armor):
    def __init__(self) -> None:
        super().__init__("Standard Skates", "+2 SPD", "🛼", Stats(speed=2))
        
    def forge(self, forge_level: int) -> ForgedArmorItem:
        return ForgedSkates(forge_level)


# FORGED ARMORS


class ForgedHelmet(ForgedHelmetItem):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Helmet", "🪖", Stats(defense=2), forge_level)


class ForgedHeadband(ForgedHelmetItem):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Headband", "🧣", Stats(defense=1, luck=2), forge_level)


class ForgedScarf(ForgedHelmetItem):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Headband", "🧣", Stats(defense=1, luck=4), forge_level)


class ForgedSkull(ForgedHelmetItem):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Skull", "💀", Stats(strength=1, defense=1), forge_level)


class ForgedTunic(ForgedArmorItem):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Tunic", "🦺", Stats(defense=2), forge_level)


class ForgedRobe(ForgedArmorItem):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Robe", "🥋", Stats(defense=1, speed=1), forge_level)


class ForgedShoes(ForgedArmorItem):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Shoes", "👟", Stats(luck=1, speed=1), forge_level)


class ForgedSkates(ForgedArmorItem):
    def __init__(self, forge_level: int) -> None:
        super().__init__("Forged Skates", "🛼", Stats(speed=2), forge_level)

