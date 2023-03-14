import nextcord
from nextcord import Interaction, ui
from typing import List, Tuple
from objects.entities import DisCharacter
from objects.items import ForgedItem
from ui.character import CharacterView
import objects.context as rpgctx
from ui.helper import ConfirmButton
from objects.rooms import Chest, Room
from ui.rooms import RoomView, RoomActions
from events.battle import Battle
from ui.storage import StorageView
from data import add_lost_gear


class Dungeon():
    player: DisCharacter
    interaction: Interaction
    message: nextcord.Message
    
    room: Room
    room_count: int
    loot_tier: int
    danger_tier: int
    
    RED = 0xe94926
    GREEN = 0x26e930
    GOLD = 0xf1c40f
    
    def __init__(self, player, interaction = Interaction, loot_tier=1, danger_tier=1):
        self.player = player
        self.interaction = interaction
        self.room_count = 0
        self.loot_tier = loot_tier
        self.danger_tier = danger_tier
        
        self.generate_room()
        
        self.survived = False
        
    def generate_room(self):
        self.room = Room(
            player=self.player, 
            loot_tier=self.loot_tier, 
            danger_tier=self.danger_tier, 
            spawn_room=self.room_count == 0
        )
        self.room_count += 1
    
    async def main(self) -> bool:
        val = await self.main_dungeon()
        if not self.survived:
            # Drop all gear
            # Forged gear loot tables
            forged = [ item for item in self.player.inventory if isinstance(item, ForgedItem) ]
            for item in forged:
                item.lost_owner = self.player.owner
                add_lost_gear(item)
            
            for item in self.player.inventory[:]:
                self.player.drop_item(item)
            
            self.player.hp = self.player.max_hp
        return val
        
    async def main_dungeon(self) -> bool:
        self.message = await self.interaction.followup.send("** **", ephemeral=True)
        
        fog_approaching = False
        while True:
            room_view = RoomView(self.room, fog_approaching=fog_approaching)
            if fog_approaching:
                await self.display_title("You will die to the fog soon", color=Dungeon.RED)
            else:
                await self.display_title(f"Room #{self.room_count}")
            await self.display_view(room_view)
            await room_view.wait()
            
            if room_view.action.action == RoomActions.EXIT:
                for item in self.player.inventory:
                    if item.lost_owner is not None:
                        item.lost_owner = None

                await self.display_text("You escaped the dungeon", color=Dungeon.GREEN)
                self.survived = True
                return True
            
            elif room_view.action.action == RoomActions.NEXT:
                self.generate_room()
            
            elif room_view.action.action == RoomActions.FIGHT:
                battle = Battle(self.player, room_view.action.payload, self.interaction)
                survival = await battle.main()
                if not survival:
                    await self.display_text("You perished in the dungeon", color=Dungeon.RED)
                    return False
                if room_view.action.payload.hp <= 0:
                    room_view.clear_tile(room_view.action.x, room_view.action.y)
            
            elif room_view.action.action == RoomActions.LOOT_CHEST:
                await self.chest_loot(room_view.action.payload)
                
            elif room_view.action.action == RoomActions.CHARACTER:
                await self.character()
                
            elif room_view.action.action == RoomActions.APPROACH_FOG:
                fog_approaching = True
            
            elif room_view.action.action == RoomActions.DIE:
                await self.display_text("You perished to the fog", color=Dungeon.RED)
                return False
    
    async def character(self):
        character_view = CharacterView(self.message, rpgctx.RPGContext(self.player))
        await character_view.update()
        await character_view.wait()
        
    async def chest_loot(self, chest: Chest):
        storage_view = StorageView(self.message, self.player, chest.contents)
        await storage_view.update()
        await storage_view.wait()
    
    async def wait_for_ok(self):
        ok_view = ConfirmButton()
        await self.display_view(ok_view)
        await ok_view.wait()
        await self.display_view(None)
    
    async def display_title(self, text: str, color: int = 0xf1c40f, keep_view=False):
        embed = nextcord.Embed(color=color)
        embed.add_field(name=text, value="", inline=False)
        await self.message.edit(embed=embed)
        
        if not keep_view:
            await self.display_view(None)
    
    async def display_text(self, text: str, color: int = 0xf1c40f, keep_view=False):
        embed = nextcord.Embed(color=color)
        embed.add_field(name="Dungeon", value=text, inline=False)
        await self.message.edit(embed=embed)
        
        if not keep_view:
            await self.display_view(None)
        
    async def display_embed(self, fields: List[Tuple[str, str]], color: int = 0xf1c40f, keep_view=False, title=None):
        embed = nextcord.Embed(color=color, title=title)
        for field in fields:
            if len(field) == 3:
                name, value, inline = field
            else:
                name, value = field
                inline = False
            embed.add_field(name=name, value=value, inline=inline)
        await self.message.edit(embed=embed)
        
        if not keep_view:
            await self.display_view(None)
    
    async def display_view(self, view: ui.View, clear=False):
        if clear:
            self.message.edit(embed=None,content="** **")
        await self.message.edit(view=view)
        
    
