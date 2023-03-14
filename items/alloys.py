from objects.items import ForgeMaterialItem

class IronAlloy(ForgeMaterialItem):
    def __init__(self) -> None:
        super().__init__("Iron Alloy", "A simple iron alloy", '🪨', 10, 1)


class BronzeAlloy(ForgeMaterialItem):
    def __init__(self) -> None:
        super().__init__("Bronze Alloy", "A simple bronze alloy", '🪨', 20, 2)


class SteelAlloy(ForgeMaterialItem):
    def __init__(self) -> None:
        super().__init__("Steel Alloy", "A strong steel alloy", '🪨', 30, 3)


class CrystalAlloy(ForgeMaterialItem):
    def __init__(self) -> None:
        super().__init__("Crystal Alloy", "A shiny crystal alloy", '🪨', 40, 5)


class PlatinumAlloy(ForgeMaterialItem):
    def __init__(self) -> None:
        super().__init__("Platinum Alloy", "A resilient platinum alloy", '🪨', 50, 6)


class TitaniumAlloy(ForgeMaterialItem):
    def __init__(self) -> None:
        super().__init__("Titanium Alloy", "An incredible titanium alloy", '🪨', 65, 8)


class MysticAlloy(ForgeMaterialItem):
    def __init__(self) -> None:
        super().__init__("Mystic Alloy", "An enticing mystical alloy", '🪨', 85, 10)


class ExoticAlloy(ForgeMaterialItem):
    def __init__(self) -> None:
        super().__init__("Exotic Alloy", "An iridescent exotic alloy", '🪨', 100, 13)
