import nextcord
import asyncio
from nextcord import Interaction
from nextcord.ext import commands
import nextcord.ui as ui
import random
from typing import List, Tuple
import math

import cogs.items as items
from cogs.entities import DisCharacter, Enemy
import cogs.context as rpgctx

TESTING_GUILDS = [658882526470864896, 811033467139784734, 1082795791476858980]

DODGE_OPTIONS = 4

class BattleActions:
    ATTACK = 1
    INVENTORY = 2
    RUN = 3
    ANALYZE = 4


def health_bar(hp, max_hp, scale=1, full=':heart:', portion=':broken_heart:', empty=':black_heart:'):
    hp /= scale
    max_hp /= scale
    return f"{full * math.floor(hp) + portion * (hp % 1 > 0) + empty * math.floor(max_hp - hp)}"


class QuicktimeEvent(ui.View):
    def __init__(self, speed: int, 
                 correct_style: nextcord.ButtonStyle, incorrect_style: nextcord.ButtonStyle, 
                 correct_emoji: str, incorrect_emoji: str,
                 option_count: int, correct_chance: float, always_possible: bool):
        super().__init__(timeout=speed)
        
        self.success = False
        self.clicked = False
        self.correct_indices = [ i for i in range(0, option_count) if random.random() < correct_chance ]
        if not self.correct_indices and always_possible:
            self.correct_indices = [ random.randint(0, option_count - 1) ]
        
        for i in range(option_count):
            btn = ui.Button()
            
            if i in self.correct_indices:
                btn.style = correct_style
                btn.emoji = correct_emoji
            else:
                btn.style = incorrect_style
                btn.emoji = incorrect_emoji
                
            btn.callback = self.build_try_event(i)
            
            self.children.append(btn)
    
    def build_try_event(self, index: int):
        async def anon(_interaction):
            await self.try_event(index)
        return anon
    
    async def try_event(self, index: int):
        self.success = index in self.correct_indices
        self.clicked = True
        self.stop()
        
    async def close(self, message: nextcord.Message):
        self.children = []
        await message.edit(view=self)


class ActionView(ui.View):
    def __init__(self):
        super().__init__()
        self.choice = BattleActions.RUN
        
    @ui.button(label="Attack", style=nextcord.ButtonStyle.success)
    async def attack(self, button: ui.Button, interaction: Interaction):
        self.choice = BattleActions.ATTACK
        self.stop()
    
    @ui.button(label="Analyze", style=nextcord.ButtonStyle.secondary)
    async def analyze(self, button: ui.Button, interaction: Interaction):
        self.choice = BattleActions.ANALYZE
        self.stop()
    
    @ui.button(label="Inventory", style=nextcord.ButtonStyle.blurple)
    async def inventory(self, button: ui.Button, interaction: Interaction):
        self.choice = BattleActions.INVENTORY
        self.stop()
    
    @ui.button(label="Flee", style=nextcord.ButtonStyle.danger)
    async def flee(self, button: ui.Button, interaction: Interaction):
        self.choice = BattleActions.RUN
        self.stop()


class ConfirmButton(ui.View):
    def __init__(self):
        super().__init__()
    
    @ui.button(label="Ok", style=nextcord.ButtonStyle.blurple)
    async def ok(self, btn: ui.Button, interaction: Interaction):
        # Ok!
        # Does nothing.
        self.stop()


class InventoryView(ui.View):
    dropdown: ui.Select
    ctx: rpgctx.RPGContext
    response = items.ItemUseResponse
    
    def __init__(self, ctx: rpgctx.RPGContext):
        super().__init__()
        
        self.response = None
        self.ctx = ctx
        
        select_options = []
        for i, item in enumerate(ctx.player.inventory):
            item: items.Item
            select_options.append(nextcord.SelectOption(
                label=item.name,
                description=item.description,
                emoji=item.emoji,
                value=str(i)
            ))
        
        self.dropdown = ui.Select(placeholder="Choose an Item", options=select_options, max_values=1)
        self.dropdown.callback = self.use_item
        self.add_item(self.dropdown)
        
        back_button = ui.Button(style=nextcord.ButtonStyle.danger, label="Back")
        back_button.callback = self.go_back
        self.add_item(back_button)
        
    async def go_back(self, interaction: Interaction):
        self.stop()
        
    async def use_item(self, interaction: Interaction):
        inv = self.ctx.player.inventory
        iter_inv = inv[:]
        for i in self.dropdown.values:
            item: items.Item = iter_inv[int(i)]
            self.response = await item.on_use(self.ctx)
            if self.response.used:
                inv.remove(item)
        self.stop()


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
                (self.player.name, health_bar(self.player.hp, self.player.max_hp, scale=2)),
                (self.enemy.name, health_bar(self.enemy.hp, self.enemy.max_hp, scale=2))
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


class Fight(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(description="Starts a test battle.", guild_ids=TESTING_GUILDS)
    async def test_battle(self, interaction: Interaction):
        player = DisCharacter(10, 0, 1, 0, 10)
        player.name = interaction.user.name
        player.inventory = [
            items.HealthPotion(),
            items.HealthPotion(),
            items.HealthPotion()
        ]
        
        enemy = Enemy(10, 0, 1, 0)
        enemy.name = "Testing Enemy"
        
        await interaction.response.defer(ephemeral=False, with_message=True)
        
        battle = Battle(player, enemy, interaction)
        await battle.main()


def setup(client: commands.Bot):
    client.add_cog(Fight(client))
