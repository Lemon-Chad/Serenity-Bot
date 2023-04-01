import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import data
import os, sys

ADMIN_GUILDS = [658882526470864896]


class AdminCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name="shutdown", description="Stops the bot.", guild_ids=ADMIN_GUILDS)
    async def shutdown(self, interaction: Interaction):
        await interaction.send("Shutting down.", ephemeral=True)
        await self.client.close()
        
    @nextcord.slash_command(name="restart", description="Restarts the bot.", guild_ids=ADMIN_GUILDS)
    async def shutdown(self, interaction: Interaction):
        await interaction.send("Shutting down.", ephemeral=True)
        await self.client.close()
        os.execv(sys.argv[0], sys.argv)

    @nextcord.slash_command(name="wipe", description="Wipes all data", guild_ids=ADMIN_GUILDS)
    async def wipe(self, interaction: Interaction):
        await interaction.send("Wiping.", ephemeral=True)
        data.wipe_data()
        data.save_data()
        await interaction.send("Wiped.", ephemeral=True)


def setup(client: commands.Bot):
    client.add_cog(AdminCommands(client))
