import random
from items import trinkets, alloys, weapons, armors, consumables


class LootTable:
    def __init__(self, *entries):
        assert len(entries) % 2 == 0, "Must be in format (item1, weight1, item2, weight2...)"
        
        self.entries = {
            entries[i * 2]: entries[i * 2 + 1]
            for i in range(round(len(entries) / 2))
        }
        
        top = sum(self.entries.values())
        self.entries = {
            k: v / top
            for (k, v) in self.entries.items()
        }
    
    def drop(self, r=None):
        if r is None:
            r = random.random()
        tail = 0
        for (k, v) in self.entries.items():
            if tail <= r < tail + v:
                return k
            tail += v
        return list(self.entries.keys())[-1]


dungeon_chest_forge_levels = [
    ( 0,  2 ),
    ( 0,  3 ),
    ( 1,  6 ),
    ( 2,  8 ),
    ( 4, 10 ),
    ( 4, 13 ),
]


dungeon_chest_tables = [
    LootTable(
        trinkets.AncientCoin, 40,
        trinkets.DirtyTrophy, 25,
        trinkets.OldRing, 25,
        weapons.StandardSword, 15,
        weapons.StandardDagger, 10,
        weapons.StandardShield, 10,
        weapons.StandardBow, 10,
        consumables.HealthPotion, 10,
        armors.StandardHelmet, 5,
        armors.StandardTunic, 5,
        alloys.IronAlloy, 5,
        alloys.BronzeAlloy, 1
    ),
    LootTable(
        trinkets.OldRing, 30,
        trinkets.DullTrident, 26,
        trinkets.CrackedStarMedallion, 20,
        consumables.HealthPotion, 15,
        weapons.StandardDagger, 15,
        weapons.StandardShield, 15,
        weapons.StandardBow, 15,
        weapons.StandardSword, 10,
        armors.StandardHelmet, 10,
        armors.StandardTunic, 10,
        alloys.IronAlloy, 10,
        consumables.Grenade, 5,
        armors.StandardHeadband, 5,
        armors.StandardRobe, 5,
        armors.StandardShoes, 5,
        alloys.BronzeAlloy, 5,
        alloys.SteelAlloy, 1
    ),
    LootTable(
        trinkets.CrackedStarMedallion, 40,
        trinkets.Crystal, 35,
        trinkets.Crown, 30,
        consumables.HealthPotion, 20,
        armors.StandardHelmet, 20,
        armors.StandardTunic, 20,
        weapons.StandardShield, 15,
        weapons.StandardBow, 15,
        alloys.IronAlloy, 15,
        armors.StandardHeadband, 10,
        armors.StandardRobe, 10,
        armors.StandardShoes, 10,
        alloys.BronzeAlloy, 10,
        consumables.Grenade, 10,
        armors.StandardScarf, 5,
        armors.StandardSkates, 5,
        armors.StandardSkull, 5,
        consumables.HealthPotionII, 5,
        alloys.SteelAlloy, 5,
        alloys.CrystalAlloy, 1,
    ),
    LootTable(
        trinkets.CrackedStarMedallion, 40,
        trinkets.Crystal, 38,
        trinkets.Crown, 36,
        consumables.HealthPotion, 25,
        armors.StandardHeadband, 15,
        armors.StandardRobe, 15,
        armors.StandardShoes, 15,
        alloys.BronzeAlloy, 15,
        consumables.Grenade, 15,
        armors.StandardScarf, 10,
        armors.StandardSkates, 10,
        armors.StandardSkull, 10,
        alloys.SteelAlloy, 10,
        consumables.HealthPotionII, 10,
        alloys.CrystalAlloy, 5,
        consumables.GrenadeII, 5,
        alloys.PlatinumAlloy, 1,
    ),
    LootTable(
        trinkets.Crystal, 40,
        trinkets.Crown, 38,
        trinkets.CrackedCrystalBall, 30,
        consumables.Grenade, 20,
        armors.StandardScarf, 15,
        armors.StandardSkates, 15,
        armors.StandardSkull, 15,
        alloys.SteelAlloy, 15,
        consumables.HealthPotionII, 15,
        consumables.GrenadeII, 10,
        alloys.CrystalAlloy, 10,
        alloys.PlatinumAlloy, 5,
        consumables.HealthPotionIII, 5,
        alloys.TitaniumAlloy, 2,
        alloys.MysticAlloy, 1,
    ),
    LootTable(
        trinkets.Crystal, 45,
        trinkets.Crown, 40,
        trinkets.CrackedCrystalBall, 38,
        trinkets.GoldBag, 25,
        consumables.HealthPotionII, 25,
        consumables.GrenadeII, 20,
        alloys.SteelAlloy, 20,
        alloys.CrystalAlloy, 15,
        consumables.HealthPotionIII, 10,
        alloys.TitaniumAlloy, 5,
        consumables.GrenadeIII, 5,
        alloys.MysticAlloy, 2,
        alloys.ExoticAlloy, 1,
    )
]
