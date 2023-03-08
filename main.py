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


class UITest(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None
        
    @nextcord.ui.button(label="Click Me!", style=nextcord.ButtonStyle.secondary)
    async def click_me(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.send("i have been clicked.")
        self.value = True
        self.stop()
        
    @nextcord.ui.button(label="Don't Click Me!", style=nextcord.ButtonStyle.success)
    async def dont_click_me(self, button: nextcord.ui.Button, interaction: Interaction):
        for _ in range(10):
            await interaction.send("WHYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
        self.value = False
        self.stop()
    


@client.event
async def on_ready():
    print("N: Annihilation Bot")
    print("V: 1.0.0a")
    print("U: March 7. 2023")
    print("C: LemonChad")
    

@client.slash_command(description="pongs", guild_ids=TESTING_GUILDS)
async def ping(interaction: Interaction):
    await interaction.send("Pong!")


@client.slash_command(description="im testing buttons", guild_ids=TESTING_GUILDS)
async def button_test(interaction: Interaction):
    view = UITest()
    await interaction.send(view=view)
    await view.wait()
    
    if view.value is None:
        await interaction.send("You must choose.")
    elif view.value:
        await interaction.send(":)")
    else:
        await interaction.send(":(")


client.run('MTA4Mjc4NjI4ODQwMDM0NzI2OA.GDcRAo.6cmH3pdmniFcPYgGW68NzAzC04T4J9clBku4Hs')
