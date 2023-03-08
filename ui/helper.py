from nextcord import ui, Interaction
import nextcord
import math


def bar(hp, max_hp, scale=1, full=':heart:', portion=':broken_heart:', empty=':black_heart:'):
    hp /= scale
    max_hp /= scale
    return f"{full * math.floor(hp) + portion * (hp % 1 > 0) + empty * math.floor(max_hp - hp)}"


class ConfirmButton(ui.View):
    def __init__(self):
        super().__init__()
    
    @ui.button(label="Ok", style=nextcord.ButtonStyle.blurple)
    async def ok(self, btn: ui.Button, interaction: Interaction):
        # Ok!
        # Does nothing.
        self.stop()
