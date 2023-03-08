from nextcord import ui, Interaction
import objects.context as rpgctx
import nextcord
from objects import items


class InventoryView(ui.View):
    dropdown: ui.Select
    ctx: rpgctx.RPGContext
    response = items.ItemUseResponse
    
    def __init__(self, ctx: rpgctx.RPGContext):
        super().__init__()
        
        self.response = None
        self.ctx = ctx
        
        select_options = []
        for i, item in enumerate(ctx.player.inventory):
            item: items.Item
            select_options.append(nextcord.SelectOption(
                label=item.name,
                description=item.description,
                emoji=item.emoji,
                value=str(i)
            ))
        
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
            item: items.Item = iter_inv[int(i)]
            self.response = await item.on_use(self.ctx)
            if self.response.used:
                inv.remove(item)
        self.stop()
    