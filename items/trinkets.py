from objects.items import GenericItem


class AncientCoin(GenericItem):
    def __init__(self) -> None:
        super().__init__("Ancient Coin", "An old coin with historical engravings", '🪙', 10)


class DirtyTrophy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Dirty Trophy", 'A trophy for "world\'s dirtiest person"', '🏆', 15)


class OldRing(GenericItem):
    def __init__(self) -> None:
        super().__init__("Old Ring", "A useless but pretty ring", '💍', 15)


class DullTrident(GenericItem):
    def __init__(self) -> None:
        super().__init__("Dull Trident", "A trident that couldn't stand the elements", '🔱', 15)
        
        
class CrackedStarMedallion(GenericItem):
    def __init__(self) -> None:
        super().__init__("Cracked Star Medallion", "A worn star medallion, now useless", '🏅', 20)


class Crystal(GenericItem):
    def __init__(self) -> None:
        super().__init__("Crystal", "A valuable crystal worth selling", '💎', 20)


class Crown(GenericItem):
    def __init__(self) -> None:
        super().__init__("Crown", "An ancient, and expensive, crown", '👑', 30)


class CrackedCrystalBall(GenericItem):
    def __init__(self) -> None:
        super().__init__("Cracked Crystal Ball", "A shiny cracked crystalline orb", '🔮', 45)


class GoldBag(GenericItem):
    def __init__(self) -> None:
        super().__init__("Gold Bag", "It's a bag o' gold!", '💰', 60)
