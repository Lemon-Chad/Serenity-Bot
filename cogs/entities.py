import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import nextcord.ui as ui
from typing import List
from cogs.items import Item


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
