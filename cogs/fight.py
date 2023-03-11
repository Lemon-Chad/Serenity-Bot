import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from events.battle import Battle
from objects import items
from objects.entities import DisCharacter, Enemy, generate_stats


TESTING_GUILDS = [658882526470864896, 811033467139784734, 1082795791476858980]


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
    
    @nextcord.slash_command(description="Starts a test battle.", guild_ids=TESTING_GUILDS)
    async def pwr_battle(self, interaction: Interaction, power: int):
        player = DisCharacter(10, 0, 1, 0, 10)
        player.name = interaction.user.name
        player.inventory = [
            items.HealthPotion(),
            items.HealthPotion(),
            items.HealthPotion()
        ]
        
        hp, defense, strength, speed = tuple(generate_stats(power))
        enemy = Enemy(hp * 5, defense, strength, speed)
        enemy.name = "Testing Enemy"
        
        await interaction.response.defer(ephemeral=False, with_message=True)
        
        battle = Battle(player, enemy, interaction)
        await battle.main()


def setup(client: commands.Bot):
    client.add_cog(Fight(client))
