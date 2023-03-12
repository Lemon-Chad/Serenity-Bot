from objects.items import GenericItem

class IronAlloy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Iron Alloy", "A simple iron alloy", '🪨', 10)


class BronzeAlloy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Bronze Alloy", "A simple bronze alloy", '🪨', 20)


class SteelAlloy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Steel Alloy", "A strong steel alloy", '🪨', 30)


class CrystalAlloy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Crystal Alloy", "A shiny crystal alloy", '🪨', 40)


class PlatinumAlloy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Platinum Alloy", "A resilient platinum alloy", '🪨', 50)


class TitaniumAlloy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Titanium Alloy", "An incredible titanium alloy", '🪨', 65)


class MysticAlloy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Mystic Alloy", "An enticing mystical alloy", '🪨', 85)


class ExoticAlloy(GenericItem):
    def __init__(self) -> None:
        super().__init__("Exotic Alloy", "An iridescent exotic alloy", '🪨', 100)
