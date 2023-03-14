import nextcord
from nextcord import ui, Interaction
from objects.account import Account
from objects.items import ForgedItem
from ui.helper import item_select_options


class SelectRenameView(ui.View):
    acc: Account
    selected: ForgedItem
    
    def __init__(self, acc: Account) -> None:
        super().__init__()
        self.selected = None
        self.acc = acc
        select_options = item_select_options(
            [ x for x in acc.player.inventory if isinstance(x, ForgedItem) ], 
            lambda x: self.acc.player.inventory.index(x)
        )
        self.dropdown = ui.Select(
            placeholder="Choose an Item",
            max_values=1,
            options=select_options,
        )
        self.dropdown.callback = self.on_submit
        self.add_item(self.dropdown)
        
    async def on_submit(self, _: Interaction):
        self.selected = self.acc.player.inventory[int(self.dropdown.values[0])]
        self.stop()

