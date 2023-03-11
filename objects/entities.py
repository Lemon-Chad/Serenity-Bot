import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import nextcord.ui as ui
from typing import List
from objects.items import Item
import random
import math


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
    return [ math.ceil(x * power_level) for x in stats ]


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
        
    def damage(self, amount):
        dmg = max(amount - self.defense, 1)
        self.hp = max(0, self.hp - dmg)
        return dmg


class DisCharacter(Fightable):
    inventory: List[Item]
    xp: float
    level: float
    name: str
    luck: float
    
    def __init__(self, hp, defense, strength, speed, luck):
        super().__init__(hp, defense, strength, speed)
        
        self.luck = luck
        
        self.xp = 0
        self.level = 1
        
        self.inventory = []
        
        self.name = "<GenericPlayer>"


class Enemy(Fightable):
    name: str
    
    def __init__(self, hp, defense, strength, speed):
        super().__init__(hp, defense, strength, speed)
        
        self.name = "<GenericEnemy>"
