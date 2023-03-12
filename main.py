import nextcord
from nextcord import Interaction
from nextcord.ext import commands, tasks
import objects.entities
import ui.helper
import objects.loot_tables
import data


with open("token.txt", "r") as f:
    token = f.read()


TESTING_GUILDS = [658882526470864896, 811033467139784734, 1082795791476858980]


class Bot(commands.Bot):
    async def async_cleanup(self):
        data.save_data()
        save_task.stop()
    
    async def close(self):
        await self.async_cleanup()
        
        await super().close()


client = Bot()

extensions = [
    "fight",
    "rooms"
]

if __name__ == "__main__":
    for ext in extensions:
        client.load_extension("cogs." + ext)
    

@client.event
async def on_ready():
    print("N: Annihilation Bot")
    print("V: 1.0.0a")
    print("U: March 7. 2023")
    print("C: LemonChad")


@client.slash_command(name="generatestats", description="Generates random stats", guild_ids=TESTING_GUILDS)
async def generate_stats(interaction: Interaction, power_lvl: int):
    await interaction.send(str(objects.entities.generate_stats(power_lvl)))
    
    
@client.slash_command(name="generatebar", description="Generates an HP bar", guild_ids=TESTING_GUILDS)
async def generate_bar(interaction: Interaction, hp: int, max_hp: int):
    await interaction.send(str(ui.helper.tiered_bar(hp, max_hp, number=True)))


@commands.is_owner()
@client.slash_command(name="shutdown", description="Stops the bot.", guild_ids=TESTING_GUILDS)
async def shutdown(interaction: Interaction):
    await interaction.send("Shutting down.", ephemeral=True)
    await client.close()


@tasks.loop(hours=6.0)
async def save_task():
    data.save_data()


save_task.start()
client.run(token)
