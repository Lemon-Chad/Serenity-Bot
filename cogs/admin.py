import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import data

TESTING_GUILDS = [658882526470864896]


class AdminCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name="shutdown", description="Stops the bot.", guild_ids=TESTING_GUILDS)
    async def shutdown(self, interaction: Interaction):
        await interaction.send("Shutting down.", ephemeral=True)
        await self.client.close()

    @nextcord.slash_command(name="wipe", description="Wipes all data", guild_ids=TESTING_GUILDS)
    async def wipe(self, interaction: Interaction):
        await interaction.send("Wiping.", ephemeral=True)
        data.wipe_data()
        data.save_data()
        await interaction.send("Wiped.", ephemeral=True)


def setup(client: commands.Bot):
    client.add_cog(AdminCommands(client))
