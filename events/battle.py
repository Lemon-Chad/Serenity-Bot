from objects.entities import DisCharacter, Enemy
from nextcord import Interaction
import nextcord
from ui.battle import ActionView, BattleActions
from ui.helper import ConfirmButton, tiered_bar
from ui.inventory import InventoryView
from events.quicktime import QuicktimeEvent
import objects.context as rpgctx
import asyncio
import math
import random
import nextcord.ui as ui
from typing import List, Tuple


class Battle():
    player: DisCharacter
    enemy: Enemy
    interaction: Interaction
    message: nextcord.Message
    
    RED = 0xe94926
    GREEN = 0x26e930
    GOLD = 0xf1c40f
    
    def __init__(self, player, enemy, interaction = Interaction):
        self.player = player
        self.enemy = enemy
        self.interaction = interaction
    
    async def main(self) -> bool:
        self.message = await self.interaction.followup.send("** **", ephemeral=True)
        
        while self.player.hp > 0 and self.enemy.hp > 0:
            await self.display_embed([
                (self.player.name, tiered_bar(self.player.hp, self.player.max_hp, number=True)),
                (self.enemy.name, tiered_bar(self.enemy.hp, self.enemy.max_hp, number=True))
            ])
            action_view = ActionView()
            await self.display_view(action_view)
            await action_view.wait()
            
            if action_view.choice == BattleActions.RUN:
                await self.display_text(f"{self.interaction.user.mention} has fled the battle!", color=Battle.RED)
                break
            
            elif action_view.choice == BattleActions.INVENTORY:
                await self.inventory()
                
            elif action_view.choice == BattleActions.ANALYZE:
                await self.analyze()
                
            elif action_view.choice == BattleActions.ATTACK:
                await self.attack()
        
        if self.player.hp <= 0:
            await self.display_text(f"{self.interaction.user.mention} has lost!", color=Battle.RED)
        elif self.enemy.hp <= 0:
            await self.display_text(f"{self.interaction.user.mention} has won!", color=Battle.GREEN)
            
        await self.wait_for_ok()
        await self.message.delete()
        return self.player.hp > 0
    
    async def analyze(self):
        if self.enemy.max_hp > 50:
            hlth = ":heart: x" + str(self.enemy.max_hp // 5 + 1)
        else:
            hlth = ":heart:"   *    (self.enemy.max_hp // 5 + 1)
        
        if self.enemy.strength > 10:
            strngth = ":star: x" + str(self.enemy.strength + 1)
        else:
            strngth = ":star:"   *    (self.enemy.strength + 1)
            
        if self.enemy.defense > 10:
            dfns = ":shield: x" + str(self.enemy.defense + 1)
        else:
            dfns = ":shield:"   *    (self.enemy.defense + 1)
            
        if self.enemy.speed > 10:
            spd = ":athletic_shoe: x" + str(self.enemy.speed + 1)
        else:
            spd = ":athletic_shoe:"   *    (self.enemy.speed + 1)
            
        await self.display_embed([
            ( "VITALITY"  , hlth   , True  ),
            ( "STRENGTH", strngth, True  ),
            ( ""        , ""     , False ),
            ( "DEFENSE" , dfns   , True  ),
            ( "SPEED"   , spd    , True  ),
        ], title=self.enemy.name)
        await self.wait_for_ok() 
    
    async def attack(self):
        player_first = random.random() <= 0.5 * (1 - math.log((self.player.speed + 1) / (self.enemy.speed + 1), 0.5))
        
        if player_first:
            await self.player_attack()
        else:
            await self.enemy_attack()
        
        if self.enemy.hp <= 0 or self.player.hp <= 0:
            return
        
        if player_first:
            await self.enemy_attack()
        else:
            await self.player_attack()
        
    async def player_attack(self):
        await self.display_text("You ready your sword...")
        await asyncio.sleep(random.random() * 1.5 + 1)
        
        # Critical hit
        event = QuicktimeEvent(2, 
                                nextcord.ButtonStyle.success, 
                                nextcord.ButtonStyle.secondary,
                                '🌟',
                                '⭐',
                                5, self.player.luck / 100, False)
        await self.display_text("Attack!")
        await self.display_view(event)
        await event.wait()
        
        dmg = 0
        if event.clicked:
            if event.success:
                dmg = self.enemy.damage(self.player.strength * 2)
                await self.display_text(f"Critical hit! :star2:\nYou dealt **{dmg} damage!**")
            else:
                dmg = self.enemy.damage(self.player.strength)
                await self.display_text(f"You dealt **{dmg} damage!**", color=Battle.GREEN)
        else:
            await self.display_text("You missed!", color=Battle.RED)
        
        await self.wait_for_ok()
    
    async def enemy_attack(self):
        await self.display_text("The enemy prepares their attack...")
        await asyncio.sleep(random.random() * 1.5 + 1)
        
        event = QuicktimeEvent(2,
                                nextcord.ButtonStyle.success, 
                                nextcord.ButtonStyle.secondary,
                                '🔄',
                                '⏹️',
                                4, 0, True)
        await self.display_text("Dodge!")
        await self.display_view(event)
        await event.wait()
        
        dmg = 0
        if event.clicked:
            if event.success:
                dodge_chance = 0.1 + 0.8 / (1 + math.exp(-4.6 * ((self.player.speed + 1) / (self.enemy.speed + 1) - 1)))
                if random.random() < dodge_chance:
                    await self.display_text(f"You fully dodged the attack!", color=Battle.GREEN)
                else:
                    dmg = self.player.damage(self.enemy.strength)
                    await self.display_text(f"You partially dodged the attack, but the enemy was faster.\nThe enemy dealt **{dmg} damage!**", color=Battle.GREEN)
            else:
                dmg = self.player.damage(self.enemy.strength)
                await self.display_text(f"You fumbled, and the enemy dealt **{dmg} damage!**")
        else:
            dmg = self.player.damage(self.enemy.strength * 2)
            await self.display_text(f"The enemy landed a perfect hit and dealt **{dmg} damage!**", color=Battle.RED)
        
        await self.wait_for_ok()
    
    async def inventory(self):
        await self.display_text("Showing Inventory...")
                
        inv_view = InventoryView(rpgctx.BattleContext(self.player, self.enemy, self))
        await self.display_view(inv_view)
        await inv_view.wait()
        
        resp = inv_view.response
        if resp != None and resp.message != None:
            color = Battle.RED
            if resp.used:
                color = Battle.GREEN
            await self.display_text(resp.message, color=color)
            await self.wait_for_ok()
    
    async def wait_for_ok(self):
        ok_view = ConfirmButton()
        await self.display_view(ok_view)
        await ok_view.wait()
        await self.display_view(None)
    
    async def display_text(self, text: str, color: int = 0xf1c40f, keep_view=False):
        embed = nextcord.Embed(color=color)
        embed.add_field(name="Battle", value=text, inline=False)
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
    
    async def display_view(self, view: ui.View):
        await self.message.edit(view=view)
