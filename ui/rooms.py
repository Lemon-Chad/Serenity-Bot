from nextcord import ui, Interaction
from objects.rooms import Room
from objects.rooms import TileType
from nextcord import ButtonStyle


class RoomActions:
    NEXT = 0
    FIGHT = 1
    LOOT_CHEST = 2
    EXIT = 3
    CHARACTER = 4
    APPROACH_FOG = 5
    DIE = 6


class RoomAction:
    action: int
    payload: any
    x: int
    y: int
    
    def __init__(self, action: int, x: int, y: int, payload: any = None) -> None:
        self.action = action
        self.payload = payload
        self.x = x
        self.y = y


class RoomView(ui.View):
    STYLE_GUIDE = {
        TileType.CHEST       : ButtonStyle.green,
        TileType.SUPER_CHEST : ButtonStyle.blurple,
        TileType.BAG         : ButtonStyle.green,
        TileType.ENEMY       : ButtonStyle.red,
        TileType.ENEMY_DOOR  : ButtonStyle.red,
        TileType.WALL        : ButtonStyle.blurple,
    }
    EMOJI_GUIDE = {
        TileType.CHEST       : '📦', 
        TileType.SUPER_CHEST : '📦', 
        TileType.ENEMY       : '💀',
        TileType.ENEMY_DOOR  : '💀',
        TileType.DOOR        : '🚪',
        TileType.EXIT        : '🚀',
        TileType.BAG         : '💰',
    }
    
    room: Room
    action: RoomAction
    
    def __init__(self, room: Room, fog_approaching=False):
        super().__init__(timeout=120)
        self.room = room
        self.action = RoomAction(RoomActions.DIE if fog_approaching else RoomActions.APPROACH_FOG, 0, 0)
        
        for y in range(room.size):
            for x in range(room.size):
                tile = room.get_tile(x, y)
                button = ui.Button(
                    label=None if tile.tile_type in RoomView.EMOJI_GUIDE else "\u200b",
                    emoji=RoomView.EMOJI_GUIDE.get(tile.tile_type,       None      ),
                    style=RoomView.STYLE_GUIDE.get(tile.tile_type, ButtonStyle.gray),
                    row=y,
                    custom_id=f'{x},{y}'
                )
                
                button.callback = self.callback_builder(x, y)
                self.add_item(button)
        
        button = ui.Button(
            label="Character",
            style=ButtonStyle.green,
            row=room.size
        )
        button.callback = self.character
        self.add_item(button)
    
    async def character(self, _: Interaction):
        self.set_action(RoomActions.CHARACTER, 0, 0)
       
    def callback_builder(self, x, y):
        async def anon(interaction: Interaction):
            await self.explore_tile(interaction, x, y)
        return anon
    
    async def explore_tile(self, _: Interaction, x: int, y: int):
        tile = self.room.get_tile(x, y)
        if tile.tile_type == TileType.DOOR:
            self.set_action(RoomActions.NEXT, x, y)
            
        elif tile.tile_type == TileType.ENEMY or tile.tile_type == TileType.ENEMY_DOOR:
            self.set_action(RoomActions.FIGHT, x, y, tile.contents)
            
        elif tile.tile_type in ( TileType.CHEST, TileType.BAG, TileType.SUPER_CHEST ):
            self.set_action(RoomActions.LOOT_CHEST, x, y, tile.contents)
            
        elif tile.tile_type == TileType.EXIT:
            self.set_action(RoomActions.EXIT, x, y)
    
    def clear_tile(self, x: int, y: int):
        self.room.clear_tile(x, y)
    
    def set_action(self, action: int, x: int, y: int, payload: any = None):
        self.stop()
        self.action = RoomAction(action, x, y, payload)
