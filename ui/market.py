import nextcord
from nextcord import ui, Interaction
from objects.account import Account
from objects.entities import DisCharacter
from objects.items import Item
from ui.helper import item_select_options


class MarketView(ui.View):
    msg: nextcord.Message
    interaction: Interaction
    acc: Account
    item_select: ui.Select
    
    message: str
    message_color: int
    
    def __init__(self, interaction: Interaction, acc: Account):
        super().__init__()
        self.interaction = interaction
        self.acc = acc
        self.message = None
        self.message_color = nextcord.ButtonStyle.green
        
    def get_selected_item(self):
        if not self.item_select.values or self.item_select.values[0] == "-1":
            return
        return self.acc.player.inventory[int(self.item_select.values[0])]
    
    async def update(self):
        self.clear_items()
        
        if self.message:
            self.add_item(ui.Button(
                style=self.message_color,
                label=self.message,
                row=0
            ))
            self.message = None
        
        options = item_select_options(self.acc.player.inventory)
        self.item_select = ui.Select(
            options=options,
            max_values=1,
            row=1,
            placeholder="Choose an Item to Sell"
        )
        self.add_item(self.item_select)
        
        sell_button = ui.Button(
            style=nextcord.ButtonStyle.green,
            label="Sell",
            row=2
        )
        sell_button.callback = self.sell_item
        self.add_item(sell_button)
        
        inspect_button = ui.Button(
            style=nextcord.ButtonStyle.gray,
            label="Inspect",
            row=2
        )
        inspect_button.callback = self.inspect_item
        self.add_item(inspect_button)
        
        back_button = ui.Button(
            style=nextcord.ButtonStyle.red,
            label="Back",
            row=2
        )
        back_button.callback = self.back
        self.add_item(back_button)
        
        await self.msg.edit(
            embed=nextcord.Embed(
                title="Balance", 
                description=f"{self.acc.money:,} 🪙", 
                color=0xf1c40f
            ),
            view=self
        )
        
    async def sell_item(self, _: Interaction):
        item = self.get_selected_item()
        
        if item is None:
            self.message = "You must select an item first"
            self.message_color = nextcord.ButtonStyle.red
            return
        
        self.acc.player.drop_item(item)
        self.acc.money += item.value
        
        self.message = f"Sold for {item.value:,} 🪙"
        self.message_color = nextcord.ButtonStyle.green
        
        await self.update()
        
    async def inspect_item(self, _: Interaction):
        item = self.get_selected_item()
        
        if item is None:
            self.message = "You must select an item first"
            self.message_color = nextcord.ButtonStyle.red
            return
        
        self.message = f"Item is worth {item.value:,} 🪙"
        self.message_color = nextcord.ButtonStyle.gray
        
        await self.update()
        
    async def back(self, _: Interaction):
        await self.msg.delete()
        self.stop()
    
    async def main(self):
        self.msg = await self.interaction.send("** **")
        await self.update()
    

