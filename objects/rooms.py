from typing import List
from data import find_lost_gear
from objects.items import Item
from objects.entities import DisCharacter, Enemy, generate_stats
import math
import random
from objects.storage import Storage
from objects.loot_tables import dungeon_chest_tables, dungeon_chest_forge_levels


class Chest:
    contents: Storage
    
    def __init__(self, *contents: List[Item], name: str = "Chest"):
        self.contents = Storage(name, 25, *contents)


class TileType:
    EMPTY = 0
    WALL  = 1
    ENEMY = 2
    CHEST = 3
    DOOR  = 4
    EXIT  = 5
    ENEMY_DOOR = 6
    BAG = 7
    SUPER_CHEST = 8
    PUZZLE = 9
    
    
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
    player: DisCharacter
    
    def __init__(self, player: DisCharacter, loot_tier=1, danger_tier=1, size=4, 
                 spawn_room=False, super_chest=False):
        self.size = size
        self.loot = loot_tier
        self.layout = [ None for _ in range(size * size) ]
        self.danger = danger_tier
        self.player = player
        
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

        if random.random() < 0.1:
            x, y = random_space()
            self.layout[x + y * size] = Tile(TileType.PUZZLE)
            
        if super_chest:
            x, y = random_space()
            
            chest = Chest(*self.get_loot(loot_tier + 2))
            
            self.layout[x + y * size] = Tile(TileType.SUPER_CHEST, chest)
            
        # Exit
        if random.random() < 0.05 and not spawn_room:
            x, y = random_space()
            self.layout[x + y * size] = Tile(TileType.EXIT)
        
        # Enemy count based on danger
        min_enemies = round(0.5 * (danger_tier - 1))
        max_enemies = min_enemies + math.ceil(danger_tier / 3)
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
        chest_count = random.randint(0, min(len(open_spaces), 3)) + (super_chest or spawn_room) * 2
        for _ in range(chest_count):
            x, y = random_space()
            
            chest = Chest(*self.get_loot(loot_tier))
            
            self.layout[x + y * size] = Tile(TileType.CHEST, chest)
            
        # Fill in rest of tiles with empty spaces
        for x, y in open_spaces:
            self.layout[x + y * size] = Tile(TileType.EMPTY)

    def get_loot(self, tier) -> List[Item]:
        loot_level = min(tier - 1, 5)
        
        loot_table = dungeon_chest_tables[loot_level]
        
        bonus_rolls = tier - loot_level - 1
        rolls = random.randint(2, 5)
        
        loot = [ loot_table.drop()() for _ in range(rolls + bonus_rolls) ]
        
        # Add lost player loot
        if random.random() < 0.01:
            g = find_lost_gear(
                self.player.owner, 
                dungeon_chest_forge_levels[loot_level][0] + bonus_rolls,
                dungeon_chest_forge_levels[loot_level][1] + bonus_rolls,
            )
            if g is not None:
                loot.append(g)
            
        return loot

    def get_tile(self, x, y) -> Tile:
        return self.layout[x + y * self.size]

    def clear_tile(self, x, y):
        i = x + y * self.size
        if self.layout[i].tile_type == TileType.ENEMY_DOOR:
            self.layout[i] = Tile(TileType.DOOR)
        elif self.layout[i].tile_type == TileType.ENEMY:
            self.layout[i] = Tile(TileType.BAG, Chest(*self.get_loot(self.loot + 1), name=self.layout[i].contents.name))
        else:
            self.layout[i] = Tile(TileType.EMPTY)
