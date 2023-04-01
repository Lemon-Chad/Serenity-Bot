import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import nextcord.ui as ui
from typing import List
from objects.items import Item
import random
import math
from objects.stats import Stats
from objects.slots import EquipSlots


def generate_stats(power_level, block_size=0.25, movement_count=1000):
    stats = [ 1, 1, 1, 1 ]
    i = 0
    while i < movement_count:
        j = random.randint(0, 3)
        k = random.choice([ x for x in range(0, 3) if x != i ])
        
        if stats[j] <= block_size:
            continue
        i += 1
        
        stats[j] -= block_size
        stats[k] += block_size
    return Stats(*[ math.ceil(x * power_level) for x in stats ])


class Fightable():
    max_hp: float
    hp: float
    defense: float
    strength: float
    speed: float
    
    def __init__(self, hp, defense, strength, speed):
        self.max_hp = hp
        self.hp = hp
        
        self.defense = defense
        
        self.strength = strength
        
        self.speed = speed
        
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        return amount
        
    def damage(self, amount):
        dmg = max(amount - self.defense, 1)
        self.hp = max(0, self.hp - dmg)
        return dmg


class DisCharacter(Fightable):
    inventory: List[Item]
    equipped: List[Item]
    
    name: str
    luck: float
    
    owner: int
    
    def __init__(self, hp, defense, strength, speed, luck, owner):
        super().__init__(hp, defense, strength, speed)
        
        self.luck = luck
        self.owner = owner
        
        self.xp = 0
        self.level = 1
        
        self.inventory = []
        self.equipped = [ None, None, None, None ]
        
        self.name = "<GenericPlayer>"
        
    def inventory_capacity(self):
        return 15
        
    def mainhand(self):
        return self.equipped[EquipSlots.MAINHAND]
    
    def offhand(self):
        return self.equipped[EquipSlots.OFFHAND]
    
    def helmet(self):
        return self.equipped[EquipSlots.HELMET]
    
    def armor(self):
        return self.equipped[EquipSlots.ARMOR]
    
    def add_stats(self, stats: Stats):
        self.max_hp += stats.health * 5
        self.defense += stats.defense
        self.strength += stats.strength
        self.speed += stats.speed
        self.luck += stats.luck
    
    def remove_stats(self, stats: Stats):
        self.max_hp -= stats.health * 5
        self.hp = min(self.hp, self.max_hp)
        self.defense -= stats.defense
        self.strength -= stats.strength
        self.speed -= stats.speed
        self.luck -= stats.luck
    
    def equip(self, *, mainhand=None, offhand=None, helmet=None, armor=None):
        if mainhand:
            self._equip(EquipSlots.MAINHAND, mainhand)
        if offhand :
            self._equip(EquipSlots.OFFHAND , offhand )
        if helmet  :
            self._equip(EquipSlots.HELMET  , helmet  )
        if armor   :
            self._equip(EquipSlots.ARMOR   , armor   )
    
    def _equip(self, slot: int, item: Item):
        if self.equipped[slot]:
            self.remove_stats(self.equipped[slot].stats)
        self.equipped[slot] = item
        self.add_stats(item.stats)
    
    def unequip(self, item: Item):
        for i, x in enumerate(self.equipped):
            if x is item:
                self.remove_stats(x.stats)
                self.equipped[i] = None
    
    def drop_item(self, item: Item):
        self.unequip(item)
        self.inventory.remove(item)
            
    def pickup(self, item: Item) -> bool:
        if len(self.inventory) == self.inventory_capacity():
            return False
        self.inventory.append(item) 
        return True       


class Enemy(Fightable):
    name: str
    
    def __init__(self, hp, defense, strength, speed):
        super().__init__(hp, defense, strength, speed)
        
        self.name = "<GenericEnemy>"
