from objects.items import GenericItem, ForgePerkMaterialItem
from objects.stats import Stats
import random


class AncientCoin(ForgePerkMaterialItem):
    def __init__(self) -> None:
        super().__init__("Ancient Coin", "An old coin with historical engravings", '🪙', 10, Stats(
            luck=random.randint(0, 3),
            health=random.randint(0, 3),
        ))


class DirtyTrophy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Dirty Trophy", 'A trophy for "world\'s dirtiest person"', '🏆', 15)


class OldRing(GenericItem):
    def __init__(self) -> None:
        super().__init__("Old Ring", "A useless but pretty ring", '💍', 15)


class DullTrident(ForgePerkMaterialItem):
    def __init__(self) -> None:
        super().__init__("Dull Trident", "A trident that couldn't stand the elements", '🔱', 15, Stats(
            speed=random.randint(0, 3),
            strength=random.randint(0, 3),
        ))
        
        
class CrackedStarMedallion(ForgePerkMaterialItem):
    def __init__(self) -> None:
        super().__init__("Cracked Star Medallion", "A worn star medallion, now useless", '🏅', 20, Stats(
            health=random.randint(1, 4),
            defense=random.randint(0, 3),
        ))


class Crystal(ForgePerkMaterialItem):
    def __init__(self) -> None:
        super().__init__("Crystal", "A valuable crystal worth selling", '💎', 20, Stats(
            health=random.randint(3, 7),
            strength=random.randint(1, 3),
        ))


class Crown(ForgePerkMaterialItem):
    def __init__(self) -> None:
        super().__init__("Crown", "An ancient, and expensive, crown", '👑', 30, Stats(
            health=random.randint(3, 7),
            defense=random.randint(1, 5),
        ))


class CrackedCrystalBall(ForgePerkMaterialItem):
    def __init__(self) -> None:
        super().__init__("Cracked Crystal Ball", "A shiny cracked crystalline orb", '🔮', 45, Stats(
            luck=random.randint(5, 10),
            speed=random.randint(2, 5),
        ))


class GoldBag(GenericItem):
    def __init__(self) -> None:
        super().__init__("Gold Bag", "It's a bag o' gold!", '💰', 60)
