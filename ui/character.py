from nextcord import ui, Interaction
import objects.context as rpgctx
import nextcord
from objects import items
from ui.helper import item_select_options, tiered_bar
from objects.slots import EquipSlots


class CharacterView(ui.View):
    dropdown: ui.Select
    ctx: rpgctx.RPGContext
    
    GOLD = 0xf1c40f
    
    def __init__(self, msg: nextcord.Message, ctx: rpgctx.RPGContext):
        super().__init__()
        
        self.msg = msg
        self.response = None
        self.selected_item = None
        self.ctx = ctx
            
    def get_equipped_button(self):
        if self.selected_item:
            self.equipped_button = ui.Button(style=nextcord.ButtonStyle.blurple, label=self.selected_item.name)
        else:
            self.equipped_button = ui.Button(style=nextcord.ButtonStyle.blurple, label="None")
    
    def render_selected_item(self, row):
        self.add_item(ui.Button(
            style=nextcord.ButtonStyle.blurple, 
            label=self.selected_item.name, 
            row=row
        ))
        self.add_item(ui.Button(
            style=nextcord.ButtonStyle.grey, 
            label=self.selected_item.description, 
            row=row
        ))
        row += 1
        
        if self.selected_item.item_type == items.ItemType.CONSUMABLE:
            use_button = ui.Button(
                style=nextcord.ButtonStyle.green, 
                label="Use", 
                row=row
            )
            use_button.callback = self.use_item
            self.add_item(use_button)
        elif self.selected_item.item_type in ( items.ItemType.WEAPON, items.ItemType.ARMOR ):
            for i, x in enumerate(["Mainhand", "Offhand", "Helmet", "Armor"]):
                if not self.selected_item.slot[i]:
                    continue
                equip_button = ui.Button(
                    style=nextcord.ButtonStyle.green, 
                    label="Equip " + x, 
                    row=row
                )
                equip_button.callback = self.equip_item_builder(i)
                self.add_item(equip_button)
            unequip_button = ui.Button(
                style=nextcord.ButtonStyle.red,
                label="Unequip",
                row=row
            )
            unequip_button.callback = self.unequip_item
            self.add_item(unequip_button)
        
        drop_button = ui.Button(
            style=nextcord.ButtonStyle.red,
            label="Drop",
            row=row
        )
        drop_button.callback = self.drop_item
        self.add_item(drop_button)
        row += 1
        return row
    
    async def update_msg(self):
        p = self.ctx.player
        
        embed = nextcord.Embed(color=CharacterView.GOLD, title=p.name, description="Character Menu")
        
        embed.add_field(name="Health", value=tiered_bar(p.hp, p.max_hp, number=True), inline=False)
        
        embed.add_field(name="__Equipped__", value="", inline=False)
        
        embed.add_field(name="Mainhand", value=self.get_equipped_name(EquipSlots.MAINHAND), inline=True)
        embed.add_field(name="Helmet"  , value=self.get_equipped_name(EquipSlots.HELMET  ), inline=True)
        embed.add_field(name="Armor"   , value=self.get_equipped_name(EquipSlots.ARMOR   ), inline=True)
        
        embed.add_field(name="", value="", inline=False)
        
        embed.add_field(name="Offhand", value=self.get_equipped_name(EquipSlots.OFFHAND), inline=True)
        
        if p.max_hp > 50:
            hlth = ":heart: x" + str(p.max_hp // 5 + 1)
        else:
            hlth = ":heart:"   *    (p.max_hp // 5 + 1)
        
        if p.strength > 10:
            strngth = ":star: x" + str(p.strength + 1)
        else:
            strngth = ":star:"   *    (p.strength + 1)
            
        if p.defense > 10:
            dfns = ":shield: x" + str(p.defense + 1)
        else:
            dfns = ":shield:"   *    (p.defense + 1)
            
        if p.speed > 10:
            spd = ":athletic_shoe: x" + str(p.speed + 1)
        else:
            spd = ":athletic_shoe:"   *    (p.speed + 1)
        
        luck = ":four_leaf_clover:" * (p.speed // 10 + 1)
           
          
        embed.add_field(name="__Stats__", value="", inline=False)
        
        embed.add_field(name="VITALITY", value=hlth, inline=True)
        embed.add_field(name="STRENGTH", value=strngth, inline=True)
        
        embed.add_field(name="", value="", inline=False)
        
        embed.add_field(name="DEFENSE", value=dfns, inline=True)
        embed.add_field(name="SPEED", value=spd, inline=True)
        
        embed.add_field(name="", value="", inline=False)
        
        embed.add_field(name="LUCK", value=luck, inline=True)
        
        await self.msg.edit(embed=embed) 
    
    def get_equipped_name(self, slot: int):
        if self.ctx.player.equipped[slot]:
            return self.ctx.player.equipped[slot].emoji + " " + self.ctx.player.equipped[slot].name
        return "None"
    
    async def update(self):
        self.clear_items()
        row = 0
        
        if isinstance(self.response, items.ItemUseResponse):
            self.add_item(ui.Button(
                style=nextcord.ButtonStyle.green if self.response.used else nextcord.ButtonStyle.red,
                label=self.response.message,
                row=row
            ))
            row += 1
        
        if self.selected_item:
            row = self.render_selected_item(row)
        
        select_options = item_select_options(self.ctx.player.inventory)
        
        self.dropdown = ui.Select(placeholder="Choose an Item", options=select_options, max_values=1, row=row)
        self.add_item(self.dropdown)
        row += 1
        
        select_button = ui.Button(style=nextcord.ButtonStyle.blurple, label="Select", row=row)
        select_button.callback = self.select_item
        self.add_item(select_button)
        
        back_button = ui.Button(style=nextcord.ButtonStyle.danger, label="Back",row=row)
        back_button.callback = self.go_back
        self.add_item(back_button)
        row += 1
        
        await self.update_msg()
        await self.msg.edit(view=self)
        
    def equip_item_builder(self, slot: int):
        async def anon(interaction: Interaction):
            await self.equip_item(interaction, slot)
        return anon    

    async def go_back(self, _: Interaction):
        self.stop()
        
    async def select_item(self, _: Interaction):
        inv = self.ctx.player.inventory
        self.response = None
        for i in self.dropdown.values:
            if i == "-1":
                continue
            self.selected_item = inv[int(i)]
        await self.update()
        
    async def use_item(self, _: Interaction):
        inv = self.ctx.player.inventory
        self.response = await self.selected_item.on_use(self.ctx)
        if self.response.used:
            inv.remove(self.selected_item)
        self.selected_item = None
        await self.update()
    
    async def equip_item(self, _: Interaction, slot: int):
        self.ctx.player.unequip(self.selected_item)
        self.ctx.player._equip(slot=slot, item=self.selected_item)
        self.response = items.ItemUseResponse.ok("Equipped " + self.selected_item.name)
        self.selected_item = None
        await self.update()
        
    async def unequip_item(self, _: Interaction):
        self.ctx.player.unequip(self.selected_item)
        self.response = items.ItemUseResponse.ok("Unequipped " + self.selected_item.name)
        self.selected_item = None
        await self.update()
        
    async def drop_item(self, _: Interaction):
        self.ctx.player.drop_item(self.selected_item)
        self.response = items.ItemUseResponse.ok("Dropped " + self.selected_item.name)
        self.selected_item = None
        await self.update()
    