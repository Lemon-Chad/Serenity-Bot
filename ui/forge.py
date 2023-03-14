import nextcord
from nextcord import ui, Interaction
from objects.account import Account
from objects.items import Item, ForgeableItem, ForgeMaterialItem, ForgePerkMaterialItem
from ui.helper import item_select_options


class ForgeFilters:
    ALL = 0
    FORGEABLE = 1
    UPGRADES = 2
    PERKS = 3
    
    FILTERS = [
        lambda x: True,
        lambda x: isinstance(x, ForgeableItem),
        lambda x: isinstance(x, ForgeMaterialItem),
        lambda x: isinstance(x, ForgePerkMaterialItem),
    ]
    FILTER_NAMES = [
        "All",
        "Forgeable",
        "Ugrades",
        "Perks"
    ]
    
    FILTER_COUNT = 4


class ForgeView(ui.View):
    acc: Account
    interaction: Interaction
    msg: nextcord.Message
    
    forge_item: ForgeableItem
    upgrade_item: ForgeMaterialItem
    perk_item: ForgePerkMaterialItem
    
    stash_filter: int
    
    dropdown: ui.Select
    
    message: str
    message_color: int
    
    GOLD = 0xf1c40f
    
    def __init__(self, acc: Account, interaction: Interaction) -> None:
        super().__init__()
        self.acc = acc
        self.interaction = interaction
        
        self.forge_item = None
        self.upgrade_item = None
        self.perk_item = None
        
        self.stash_filter = ForgeFilters.ALL
        
        self.message = None
        self.message_color = nextcord.ButtonStyle.green
    
    async def next_filter(self, _: Interaction):
        self.stash_filter = (self.stash_filter + 1) % ForgeFilters.FILTER_COUNT
        await self.update()
    
    def get_selected_item(self) -> Item:
        if not self.dropdown.values or self.dropdown.values[0] == "-1":
            return None
        return self.acc.player.inventory[int(self.dropdown.values[0])]
    
    async def update(self):
        self.clear_items()
        
        if self.message:
            self.add_item(ui.Button(
                label=self.message,
                style=self.message_color,
                row=0
            ))
            self.message = None
        
        filter_button = ui.Button(
            label="Filter: " + ForgeFilters.FILTER_NAMES[self.stash_filter],
            style=nextcord.ButtonStyle.blurple,
            row=1
        )
        filter_button.callback = self.next_filter
        self.add_item(filter_button)
        
        select_options = item_select_options(
            [ x for x in self.acc.player.inventory if ForgeFilters.FILTERS[self.stash_filter](x) ],
            val=lambda x: self.acc.player.inventory.index(x)
        )
        self.dropdown = ui.Select(
            placeholder="Choose an Item to Forge",
            max_values=1,
            row=2,
            options=select_options
        )
        self.add_item(self.dropdown)
        
        forge_button = ui.Button(
            label="Forge",
            style=nextcord.ButtonStyle.green,
            row=3
        )
        forge_button.callback = self.forge
        self.add_item(forge_button)
        
        self.add_use_button("Set Forge Item", self.set_forge_item)
        self.add_use_button("Set Upgrade Item", self.set_upgrade_item)
        self.add_use_button("Set Perk Item", self.set_perk_item)
        
        reset_button = ui.Button(
            label="Reset",
            style=nextcord.ButtonStyle.red,
            row=3
        )
        reset_button.callback = self.clear_forge
        self.add_item(reset_button)
        
        back_button = ui.Button(
            label="Back",
            style=nextcord.ButtonStyle.red,
            row=4
        )
        back_button.callback = self.go_back
        self.add_item(back_button)
        
        embed = nextcord.Embed(
            title="Forge",
            color=ForgeView.GOLD,
        )
        embed.add_field(name="Target", value=ForgeView.format_item(self.forge_item), inline=True)
        embed.add_field(name="Upgrade", value=ForgeView.format_item(self.upgrade_item), inline=True)
        embed.add_field(name="Perk", value=ForgeView.format_item(self.perk_item), inline=True)
        embed.add_field(name="Cost", value=f"{self.forge_cost():,} 🪙", inline=True)
        embed.add_field(name="Balance", value=f"{self.acc.money:,} 🪙", inline=False)
        
        await self.msg.edit(embed=embed, view=self)
    
    def forge_cost(self):
        return 10 * (ForgeView.item_value(self.forge_item) + ForgeView.item_value(self.upgrade_item) + ForgeView.item_value(self.perk_item))
    
    def item_value(item: Item):
        if item is None:
            return 0
        return item.value
    
    def format_item(item: Item):
        if item is None:
            return "None"
        return item.emoji + ' ' + item.name
    
    async def forge(self, _: Interaction):
        # Guards
        if self.forge_item is None:
            await self.error_message("You must have a target item")
            return
        if self.upgrade_item is None:
            await self.error_message("You must have an upgrade item")
            return
        if self.forge_cost() > self.acc.money:
            await self.error_message("You cannot afford the cost")
            return
            
        self.acc.player.drop_item(self.forge_item)
        self.acc.player.drop_item(self.upgrade_item)
        if self.perk_item is not None:
            self.acc.player.drop_item(self.perk_item)
        
        self.acc.money -= self.forge_cost()
        
        new_item = self.forge_item.forge(self.upgrade_item.forge_level)
        
        # TODO: Add forge perks
        # new_item.add_perk(self.perk_item.perk)
        
        self.acc.player.pickup(new_item)
        
        await self.clear_forge()
    
    async def clear_forge(self, _: Interaction = None):
        self.forge_item = None
        self.perk_item = None
        self.upgrade_item = None
        await self.update()
    
    async def go_back(self, _: Interaction):
        await self.msg.delete()
        self.stop()
    
    async def needs_item_message(self):
        await self.error_message("You must select an item")
    
    async def error_message(self, text):
        self.message = text
        self.message_color = nextcord.ButtonStyle.red
        await self.update()
        
    async def set_forge_item(self, _: Interaction):
        i = self.get_selected_item()
        if i is None:
            await self.needs_item_message()
            return
        if not isinstance(i, ForgeableItem):
            await self.error_message("Item cannot be forged")
            return
        self.forge_item = i
        await self.update()
        
    async def set_upgrade_item(self, _: Interaction):
        i = self.get_selected_item()
        if i is None:
            await self.needs_item_message()
            return
        if not isinstance(i, ForgeMaterialItem):
            await self.error_message("Item cannot be used to upgrade")
            return
        self.upgrade_item = i
        await self.update()
        
    async def set_perk_item(self, _: Interaction):
        i = self.get_selected_item()
        if i is None:
            await self.needs_item_message()
            return
        if not isinstance(i, ForgePerkMaterialItem):
            await self.error_message("Item cannot be used to add perks")
            return
        self.perk_item = i
        await self.update()
    
    def add_use_button(self, text, callback):
        button = ui.Button(
            label=text,
            style=nextcord.ButtonStyle.blurple,
            row=3
        )
        button.callback = callback
        self.add_item(button)
        
    async def main(self):
        self.msg = await self.interaction.send("** **", ephemeral=True)
        await self.update()
