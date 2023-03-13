import nextcord
from nextcord import ui, Interaction
from objects.entities import DisCharacter
from objects.storage import Storage
from ui.helper import item_select_options
import math


class StorageView(ui.View):
    player: DisCharacter
    storage: Storage
    message: nextcord.Message
    alert: str
    
    def __init__(self, message: nextcord.Message, player: DisCharacter, storage: Storage):
        super().__init__()
        self.player = player
        self.storage = storage
        self.message = message
        self.page = 0
        self.alert = None
        
        self.update_children()

    async def do_nothing(self, _: Interaction):
        return "lol"

    async def prev_page(self, _: Interaction):
        self.page -= 1
        await self.update()

    async def next_page(self, _: Interaction):
        self.page += 1
        await self.update()

    def update_children(self):
        self.clear_items()
        pages = math.ceil(len(self.storage.items) / 25) - 1
        
        self.add_item(ui.Button(
            label=self.storage.name + f" ({len(self.storage.items)}/{self.storage.size})",
            style=nextcord.ButtonStyle.blurple,
            row=0
        ))
        if pages > 0:
            prev_button = ui.Button(
                label='◀️',
                style=nextcord.ButtonStyle.blurple,
                row=0
            )
            if self.page == 0:
                prev_button.style = nextcord.ButtonStyle.grey
                prev_button.callback = self.do_nothing
            else:
                prev_button.callback = self.prev_page
            self.add_item(prev_button)
            
            next_button = ui.Button(
                label='▶️',
                style=nextcord.ButtonStyle.blurple,
                row=0
            )
            if self.page == pages:
                next_button.style = nextcord.ButtonStyle.grey
                next_button.callback = self.do_nothing
            else:
                next_button.callback = self.next_page
            self.add_item(next_button)
        
        storage_options = item_select_options(
            list(sorted(self.storage.items, key=lambda x: x.name))[ self.page * 25 : (self.page + 1) * 25 ],
            val=lambda x: self.storage.items.index(x)
        )
        self.storage_select = ui.Select(
            max_values=1,
            placeholder="Choose an item to transfer",
            options=storage_options,
            row=1
        )
        self.storage_select.callback = self.storage_to_inv
        self.add_item(self.storage_select)
        
        self.add_item(ui.Button(
            label=self.player.name + f" ({len(self.player.inventory)}/{self.player.inventory_capacity()})",
            style=nextcord.ButtonStyle.blurple,
            row=2
        ))
        
        inventory_options = item_select_options(self.player.inventory)
        self.inventory_select = ui.Select(
            max_values=1,
            placeholder="Choose an item to transfer",
            options=inventory_options,
            row=3
        )
        self.inventory_select.callback = self.inv_to_storage
        self.add_item(self.inventory_select)
        
        if self.alert:
            self.add_item(ui.Button(
                label=self.alert,
                style=nextcord.ButtonStyle.grey,
                row=4
            ))
        
        back_button = ui.Button(
            label="Back",
            style=nextcord.ButtonStyle.red,
            row=4
        )
        back_button.callback = self.go_back
        self.add_item(back_button)

    async def go_back(self, _: Interaction):
        self.stop()

    async def update(self):
        self.update_children()
        await self.message.edit(view=self)

    async def inv_to_storage(self, _: Interaction):
        for i in self.inventory_select.values:
            if i == "-1":
                return
            selected_item = self.player.inventory[int(i)]
        if not self.storage.insert_item(selected_item):
            self.alert = "Storage is full"
        else:
            self.player.drop_item(selected_item)
        await self.update()
    
    async def storage_to_inv(self, _: Interaction):
        for i in self.storage_select.values:
            if i == "-1":
                return
            selected_item = self.storage.items[int(i)]
        if not self.player.pickup(selected_item):
            self.alert = "Inventory is full"
        else:
            self.storage.take_item(selected_item)
        await self.update()
