
class Stats:
    health: int
    defense: int
    strength: int
    speed: int
    
    def __init__(self, health: int, defense: int, strength: int, speed: int):
        self.health = health
        self.defense = defense
        self.strength = strength
        self.speed = speed
        
    def __iter__(self):
        for i in [ self.health, self.defense, self.strength, self.speed ]:
            yield i
