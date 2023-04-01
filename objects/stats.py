
class Stats:
    health: int
    defense: int
    strength: int
    speed: int
    luck: int
    
    def __init__(self, health: int = 0, defense: int = 0, strength: int = 0, speed: int = 0, luck: int = 0):
        self.health = health
        self.defense = defense
        self.strength = strength
        self.speed = speed
        self.luck = luck
    
    def __add__(self, other):
        return Stats(
            self.health   + other.health  ,
            self.defense  + other.defense ,
            self.strength + other.strength,
            self.speed    + other.speed   ,
            self.luck     + other.luck    ,
        )
    
    def __iter__(self):
        for i in [ self.health, self.defense, self.strength, self.speed ]:
            yield i
