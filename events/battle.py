from objects.entities import DisCharacter, Enemy
from nextcord import Interaction
import nextcord
from ui.battle import ActionView, BattleActions
from ui.helper import ConfirmButton, bar
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
    
    async def main(self):
        self.message = await self.interaction.followup.send("** **")
        
        while self.player.hp > 0 and self.enemy.hp > 0:
            await self.display_embed([
                (self.player.name, bar(self.player.hp, self.player.max_hp, scale=2)),
                (self.enemy.name, bar(self.enemy.hp, self.enemy.max_hp, scale=2))
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
    
    async def analyze(self):
        await self.display_embed([
            ( "STRENGTH", ":star:"          * (1 + self.enemy.strength) ),
            ( "DEFENSE" , ":shield:"        * (1 + self.enemy.defense)  ),
            ( "SPEED"   , ":athletic_shoe:" * (1 + self.enemy.speed)    ),
        ], title=self.enemy.name, inline=True)
        await self.wait_for_ok() 
    
    async def attack(self):
        await self.player_attack()
        
        if self.enemy.hp <= 0 or self.player.hp <= 0:
            return
        
        await self.enemy_attack()
        
    async def player_attack(self):
        await self.display_text("You ready your sword...")
        await asyncio.sleep(random.random() * 1.5 + 1)
        
        # Critical hit
        event = QuicktimeEvent(1, 
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
        
        event = QuicktimeEvent(1,
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
        
    async def display_embed(self, fields: List[Tuple[str, str]], color: int = 0xf1c40f, keep_view=False, title=None, inline=False):
        embed = nextcord.Embed(color=color, title=title)
        for (name, value) in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await self.message.edit(embed=embed)
        
        if not keep_view:
            await self.display_view(None)
    
    async def display_view(self, view: ui.View):
        await self.message.edit(view=view)
