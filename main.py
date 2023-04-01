import random
import nextcord
from nextcord import Interaction
from nextcord.ext import commands, tasks
from events.dungeon import Dungeon
from ui.forge import ForgeView
from ui.itemrename import SelectRenameView
from ui.market import MarketView
from objects.account import Account
from ui.character import CharacterView
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
        data.create_account(acc.user, acc)
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
    "admin"
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


def menu(name: str):
    def decorator(func):
        async def new_func(interaction: Interaction):
            acc: Account = find_account(interaction)
            
            if acc.in_dungeon:
                await interaction.send(embed=simple_embed(
                    name, 
                    "Cannot access while in dungeon",
                    Colors.RED
                ), ephemeral=True)
                return
            if acc.in_menu:
                await acc.close_menu()
            
            acc.in_menu = True
            v = await func(acc, interaction)
            acc.in_menu = False
            
            return v
        return new_func
    return decorator


@client.event
async def on_ready():
    print("N: Annihilation Bot")
    print("V: 1.0.0a")
    print("U: March 7. 2023")
    print("C: LemonChad")
    

@client.slash_command(name="market", description="Allows you to sell items from your inventory", guild_ids=TESTING_GUILDS)
@menu(name="Market")
async def market(acc: Account, interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    
    market_view = acc.open_menu(MarketView(interaction, acc))
    await market_view.main()
    await market_view.wait()


@client.slash_command(name="forge", description="Allows you to vastly upgrade your gear", guild_ids=TESTING_GUILDS)
@menu(name="Forge")
async def forge(acc: Account, interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    
    forge_view = acc.open_menu(ForgeView(acc, interaction))
    await forge_view.main()
    await forge_view.wait()


@client.slash_command(name="stash", description="Manage your stash", guild_ids=TESTING_GUILDS)
@menu(name="Stash")
async def stash(acc: Account, interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    
    msg = await interaction.send("** **")
    s_view = acc.open_menu(StorageView(msg, acc.player, acc.stash))
    await s_view.update()
    await s_view.wait()
    await msg.delete()


@client.slash_command(name="balance", description="View your current balance", guild_ids=TESTING_GUILDS)
async def balance(interaction: Interaction):
    acc: Account = find_account(interaction)
    
    await interaction.send(embed=simple_embed(
        title="Balance",
        description=f"{acc.money:,} 🪙",
        color=Colors.GOLD
    ))


@client.slash_command(name="rename", description="Rename a forged item for 10 🪙", guild_ids=TESTING_GUILDS)
async def rename_item(interaction: Interaction, name: str):
    acc: Account = find_account(interaction)
    
    if acc.money < 10:
        await interaction.send(
            embed=simple_embed(
                title="Rename",
                description="You cannot afford this expense",
                color=Colors.RED
            ), ephemeral=True
        )
        return
    
    msg = await interaction.send(
        embed=simple_embed(
            title="Rename",
            description="Choose an item to rename",
            color=Colors.GOLD,
        ), ephemeral=True
    )
    
    r_view = SelectRenameView(acc)
    await msg.edit(view=r_view)
    await r_view.wait()
    await msg.delete()
    
    if r_view.selected is None:
        await interaction.send(
            embed=simple_embed(
                title="Rename",
                description="You must select an item",
                color=Colors.RED
            ), ephemeral=True
        )
        return
    
    r_view.selected.name = name
    acc.money -= 10
    
    await interaction.send(
        embed=simple_embed(
            title="Rename",
            description="Item renamed successfully",
            color=Colors.GREEN
        ), ephemeral=True
    )


@client.slash_command(name="character", description="Manage your character", guild_ids=TESTING_GUILDS)
@menu(name="Character")
async def character(acc: Account, interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    
    msg = await interaction.send("** **")
    c_view = acc.open_menu(CharacterView(msg, rpgctx.RPGContext(acc.player)))
    await c_view.update()
    await c_view.wait()
    await msg.delete()


DUNGEON_TIERS = [
    "1⭐",
    "2⭐",
    "3⭐",
    "1🌟",
    "2🌟",
    "3🌟",
]


@client.slash_command(name="adventure", description="Finds a dungeon", guild_ids=TESTING_GUILDS)
async def adventure(interaction: Interaction, difficulty: int = nextcord.SlashOption(
    name="difficulty",
    choices={
        x: i + 1
        for i, x in enumerate(DUNGEON_TIERS)
    }
)):
    acc = find_account(interaction)
    
    if acc.in_dungeon:
        await interaction.send(embed=simple_embed(
            "Dungeon", 
            "You are already in a dungeon",
            Colors.RED
        ), ephemeral=True)
        return
    
    if acc.in_menu:
        await interaction.send(embed=simple_embed(
            "Dungeon", 
            "You are currently in an active menu",
            Colors.RED
        ), ephemeral=True)
        return
    
    await interaction.send(embed=simple_embed(
        "Dungeon", 
        f"{interaction.user.mention} is entering a **{DUNGEON_TIERS[difficulty - 1]}** dungeon",
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

    embed = nextcord.Embed(title="Dungeon")
    if dungeon.survived:
        embed.color = Dungeon.GREEN
        embed.description = f"{interaction.user.mention} escaped a dungeon after {dungeon.room_count} rooms"
    else:
        embed.color = Dungeon.RED
        embed.description = f"{interaction.user.mention} perished in a dungeon after {dungeon.room_count} rooms"
    await interaction.send(embed=embed, ephemeral=False)


@tasks.loop(hours=6.0)
async def save_task():
    data.save_data()


save_task.start()
client.run(token)
