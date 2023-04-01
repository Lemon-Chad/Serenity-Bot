import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import data
import os
import sys
import threading
import time
import git


ADMIN_GUILDS = [658882526470864896]


class AdminCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name="shutdown", description="Stops the bot.", guild_ids=ADMIN_GUILDS)
    async def shutdown(self, interaction: Interaction):
        await interaction.send("Shutting down.", ephemeral=True)
        await self.client.close()
        
    def wait_for_start(delay: int, program: str):
        time.sleep(delay)
        
        print("Updating...")
        g = git.cmd.Git(os.getcwd())
        g.pull()
        
        print("Restarting...")
        os.execv(sys.executable, [program] + sys.argv)
    
    def git_pull():
        os.execl(os.getcwd(), "git", "pull")
        
    @nextcord.slash_command(name="restart", description="Restarts the bot.", guild_ids=ADMIN_GUILDS)
    async def restart(self, interaction: Interaction, program: str = 'python3'):
        await interaction.send("Shutting down.", ephemeral=True)
        
        t = threading.Thread(target=lambda: AdminCommands.wait_for_start(2, program))
        t.start()
        
        await self.client.close()

    @nextcord.slash_command(name="wipe", description="Wipes all data", guild_ids=ADMIN_GUILDS)
    async def wipe(self, interaction: Interaction):
        await interaction.send("Wiping.", ephemeral=True)
        data.wipe_data()
        data.save_data()
        await interaction.send("Wiped.", ephemeral=True)


def setup(client: commands.Bot):
    client.add_cog(AdminCommands(client))
