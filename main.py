import random
import nextcord
from nextcord import Interaction
from nextcord.ext import commands, tasks
from events.dungeon import Dungeon
from objects.account import Account
import objects.entities
from ui.character import CharacterView
import ui.helper
import objects.loot_tables
import data
from ui.storage import StorageView
import objects.context as rpgctx


with open("token.txt", "r") as f:
    token = f.read()


TESTING_GUILDS = [658882526470864896, 811033467139784734, 1082795791476858980]


def find_account(interaction: Interaction) -> Account:
    user_id = interaction.user.id
    if not data.has_account(user_id):
        acc = Account(interaction.user)
        data.create_account(user_id, acc)
    return data.get_account(user_id)


class Client(commands.Bot):
    async def async_cleanup(self):
        data.save_data()
        save_task.stop()
    
    async def close(self):
        await self.async_cleanup()
        
        await super().close()


client = Client()

extensions = [
    "fight",
    "rooms"
]

if __name__ == "__main__":
    for ext in extensions:
        client.load_extension("cogs." + ext)


class Colors:
    RED = 0xe94926
    GREEN = 0x26e930
    GOLD = 0xf1c40f


def simple_embed(title: str, description: str, color: int) -> nextcord.Embed:
    embed = nextcord.Embed(title=title, description=description, color=color)
    return embed


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
    
    
@client.slash_command(name="stash", description="Manage your stash", guild_ids=TESTING_GUILDS)
async def stash(interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    acc = find_account(interaction)
    
    if acc.in_dungeon:
        await interaction.send("Cannot access stash in dungeon!")
        return
    
    msg = await interaction.send("** **")
    s_view = StorageView(msg, acc.player, acc.stash)
    await s_view.update()
    await s_view.wait()
    await msg.delete()
    
    
@client.slash_command(name="character", description="Manage your character", guild_ids=TESTING_GUILDS)
async def character(interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    acc = find_account(interaction)
    
    if acc.in_dungeon:
        await interaction.send("Cannot access character in dungeon!")
        return
    
    msg = await interaction.send("** **")
    c_view = CharacterView(msg, rpgctx.RPGContext(acc.player))
    await c_view.update()
    await c_view.wait()
    await msg.delete()
    
    
@client.slash_command(name="adventure", description="Finds a dungeon", guild_ids=TESTING_GUILDS)
async def adventure(interaction: Interaction, difficulty: int = nextcord.SlashOption(
    name="difficulty",
    choices={
        "⭐": 1,
        "⭐⭐": 2,
        "⭐⭐⭐": 3,
        "⭐⭐⭐⭐": 4,
        "⭐⭐⭐⭐⭐": 5,
        "🌟🌟🌟🌟🌟🌟": 6
    }
)):
    acc = find_account(interaction)
    
    if acc.in_dungeon:
        await interaction.send("You are already in a dungeon!")
        return
    
    tiers = [
        "⭐",
        "⭐⭐",
        "⭐⭐⭐",
        "⭐⭐⭐⭐",
        "⭐⭐⭐⭐⭐",
        "🌟🌟🌟🌟🌟🌟",
    ]
    
    await interaction.send(embed=simple_embed(
        "Dungeon", 
        f"{interaction.user.mention} is entering a {tiers[difficulty - 1]} dungeon",
        Colors.GOLD
    ))
    loot_tier = difficulty
    danger_tier = difficulty
    dungeon = Dungeon(
        player=acc.player,
        interaction=interaction,
        loot_tier=loot_tier,
        danger_tier=danger_tier
    )
    
    acc.in_dungeon = True
    await dungeon.main()
    acc.in_dungeon = False


@tasks.loop(hours=6.0)
async def save_task():
    data.save_data()


save_task.start()
client.run(token)
