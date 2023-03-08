import nextcord
from nextcord import Interaction
from nextcord.ext import commands


TESTING_GUILDS = [658882526470864896, 811033467139784734, 1082795791476858980]

client = commands.Bot()

extensions = [
    "fight"
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


client.run('MTA4Mjc4NjI4ODQwMDM0NzI2OA.GDcRAo.6cmH3pdmniFcPYgGW68NzAzC04T4J9clBku4Hs')
