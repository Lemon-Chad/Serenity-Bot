import nextcord
from nextcord import ui, Interaction


class BattleActions:
    ATTACK = 1
    INVENTORY = 2
    RUN = 3
    ANALYZE = 4


class ActionView(ui.View):
    def __init__(self):
        super().__init__()
        self.choice = BattleActions.RUN
        
    @ui.button(label="Attack", style=nextcord.ButtonStyle.success)
    async def attack(self, _: ui.Button, interaction: Interaction):
        self.choice = BattleActions.ATTACK
        self.stop()
    
    @ui.button(label="Analyze", style=nextcord.ButtonStyle.secondary)
    async def analyze(self, _: ui.Button, interaction: Interaction):
        self.choice = BattleActions.ANALYZE
        self.stop()
    
    @ui.button(label="Inventory", style=nextcord.ButtonStyle.blurple)
    async def inventory(self, _: ui.Button, interaction: Interaction):
        self.choice = BattleActions.INVENTORY
        self.stop()
    
    @ui.button(label="Flee", style=nextcord.ButtonStyle.danger)
    async def flee(self, _: ui.Button, interaction: Interaction):
        self.choice = BattleActions.RUN
        self.stop()
