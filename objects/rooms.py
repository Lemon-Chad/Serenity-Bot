from typing import List
from objects.items import Item, Sword, HealthPotion, Crystal
from objects.entities import Enemy, generate_stats
import math
import random
from objects.storage import Storage


class Chest:
    contents: Storage
    
    def __init__(self, *contents: List[Item]):
        self.contents = Storage("Chest", 25, *contents)


class TileType:
    EMPTY = 0
    WALL  = 1
    ENEMY = 2
    CHEST = 3
    DOOR  = 4
    EXIT  = 5
    ENEMY_DOOR = 6
    
    
class Tile:
    tile_type: int
    contents: any
    
    def __init__(self, tile_type: int, contents: any = None) -> None:
        self.tile_type = tile_type
        self.contents = contents


class Room:
    size: int
    layout: List[Tile]
    danger: int
    loot: int
    
    def __init__(self, loot_tier=1, danger_tier=1, size=4):
        self.size = size
        self.loot = loot_tier
        self.layout = [ None for _ in range(size * size) ]
        self.danger = danger_tier
        
        open_spaces = [ (x, y) for x in range(size) for y in range(size) ]
        
        def random_space():
            x, y = random.choice(open_spaces)
            open_spaces.remove((x, y))
            return x, y
        
        # Next room doors
        door_count = 1
        if random.random() < 0.05:
            door_count = 2
            if random.random() < 0.05:
                door_count = 3
        
        open_doors = []
        for _ in range(door_count):
            x, y = random_space()
            self.layout[x + y * size] = Tile(TileType.DOOR)
            open_doors.append((x, y))
            
        # Exit
        if random.random() < 0.05:
            x, y = random_space()
            self.layout[x + y * size] = Tile(TileType.EXIT)
        
        # Enemy count based on danger
        min_enemies = round(0.5 * (danger_tier - 1))
        max_enemies = min_enemies + math.ceil(danger_tier / 6)
        enemy_count = min(len(open_spaces), random.randint(min_enemies, max_enemies))
        
        # Generates enemies in random positions
        # Enemies will always block the doors
        for _ in range(enemy_count):
            if open_doors:
                x, y = open_doors.pop()
                tile_type = TileType.ENEMY_DOOR
            else:
                x, y = random_space()
                tile_type = TileType.ENEMY
        
            hp, defense, strength, speed = generate_stats(danger_tier)
            self.layout[x + y * size] = Tile(tile_type, Enemy(hp * 5, defense, strength, speed))
        
        # Generates chests in random positions
        chest_count = random.randint(0, min(len(open_spaces), 2))
        for _ in range(chest_count):
            x, y = random_space()
            
            # Fixed loot for now
            # TODO Loot tables
            chest = Chest(
                Sword(), 
                HealthPotion(), HealthPotion(),
                Crystal()
            )
            
            self.layout[x + y * size] = Tile(TileType.CHEST, chest)
            
        # Fill in rest of tiles with empty spaces
        for x, y in open_spaces:
            self.layout[x + y * size] = Tile(TileType.EMPTY)

    def get_tile(self, x, y) -> Tile:
        return self.layout[x + y * self.size]

    def clear_tile(self, x, y):
        i = x + y * self.size
        if self.layout[i].tile_type == TileType.ENEMY_DOOR:
            self.layout[i] = Tile(TileType.DOOR)
        else:
            self.layout[i] = Tile(TileType.EMPTY)
