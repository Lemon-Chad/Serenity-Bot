import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from objects.rooms import Room, TileType
from ui.character import CharacterView
from ui.rooms import RoomView
from items import weapons, consumables, trinkets
from objects.context import RPGContext
from objects.entities import DisCharacter
from events.dungeon import Dungeon


TESTING_GUILDS = [658882526470864896, 811033467139784734, 1082795791476858980]


class RoomCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @nextcord.slash_command(description="Opens a test dungeon.", guild_ids=TESTING_GUILDS)
    async def test_dungeon(self, interaction: Interaction, loot_tier: int, danger_tier: int):
        p = DisCharacter(20, 5, 3, 2, 10, interaction.user)
        p.inventory = [
            weapons.StandardSword(),
            consumables.HealthPotion(),
            consumables.HealthPotion(),
            trinkets.Crystal(),
        ]
        
        dungeon = Dungeon(p, interaction, loot_tier=loot_tier, danger_tier=danger_tier)
        
        await interaction.response.defer(ephemeral=True, with_message=True)
        
        await dungeon.main()
        
        embed = nextcord.Embed(title="Dungeon")
        if dungeon.survived:
            embed.color = Dungeon.GREEN
            embed.description = f"{interaction.user.mention} escaped a dungeon after {dungeon.room_count} rooms."
        else:
            embed.color = Dungeon.RED
            embed.description = f"{interaction.user.mention} perished in a dungeon after {dungeon.room_count} rooms."
        await interaction.send(embed=embed, ephemeral=False)


def setup(client: commands.Bot):
    client.add_cog(RoomCommands(client))
