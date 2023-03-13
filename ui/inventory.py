from nextcord import ui, Interaction
import objects.context as rpgctx
import nextcord
from objects import items
from ui.helper import item_select_options


class InventoryView(ui.View):
    dropdown: ui.Select
    ctx: rpgctx.RPGContext
    response = items.ItemUseResponse
    
    def __init__(self, ctx: rpgctx.RPGContext):
        super().__init__()
        
        self.response = None
        self.ctx = ctx
        
        select_options = item_select_options([ 
            item 
            for item in self.ctx.player.inventory 
            if item.item_type == items.ItemType.CONSUMABLE
        ], val=lambda x: self.ctx.player.inventory.index(x))
        
        self.dropdown = ui.Select(placeholder="Choose an Item", options=select_options, max_values=1)
        self.dropdown.callback = self.use_item
        self.add_item(self.dropdown)
        
        back_button = ui.Button(style=nextcord.ButtonStyle.danger, label="Back")
        back_button.callback = self.go_back
        self.add_item(back_button)
        
    async def go_back(self, interaction: Interaction):
        self.stop()
        
    async def use_item(self, interaction: Interaction):
        inv = self.ctx.player.inventory
        iter_inv = inv[:]
        for i in self.dropdown.values:
            if i == "-1":
                return
            item: items.Item = iter_inv[int(i)]
            self.response = await item.on_use(self.ctx)
            if self.response.used:
                inv.remove(item)
        self.stop()
    