from nextcord import ui, Interaction
import nextcord
import math


def bar(hp, max_hp, scale=1, full=':heart:', portion=':broken_heart:', empty=':black_heart:'):
    if hp <= 0:
        return max_hp * empty
    hp /= scale
    max_hp /= scale
    return f"{full * math.floor(hp) + portion * (hp % 1 > 0) + empty * math.floor(max_hp - hp)}"


def item_select_options(item_list, val=None):
    if val is None:
        val = lambda x: item_list.index(x)
    select_options = []
    for item in sorted(item_list, key=lambda x: x.name):
        select_options.append(nextcord.SelectOption(
            label=item.name,
            description=item.description,
            emoji=item.emoji,
            value=str(val(item))
        ))
    
    if not select_options:
        select_options.append(nextcord.SelectOption(
            label="Nothing",
            value="-1",
            description="It's nothing",
            emoji='🕸️'
        ))
    return select_options


def tiered_bar(hp, max_hp, tiers=None, upgrade_level=5, number=False):
    if tiers is None:
        tiers = [
            ":black_heart:",
            ":heart:",
            ":orange_heart:",
            ":yellow_heart:",
            ":green_heart:",
            ":blue_heart:",
            ":purple_heart:",
            ":red_square:",
            ":orange_square:",
            ":yellow_square:",
            ":green_square:",
            ":blue_square:",
            ":purple_square:",
            ":red_circle:",
            ":orange_circle:",
            ":yellow_circle:",
            ":green_circle:",
            ":blue_circle:",
            ":purple_circle:",
        ]
    
    if hp <= 0:
        return tiers[0] * upgrade_level
    
    level = hp // upgrade_level
    if level >= len(tiers):
        level %= len(tiers)
        nlevel = level - 1
        if nlevel == -1:
            nlevel = len(tiers) - 2
    else:
        nlevel = level - 1
    
    level_hp = hp % upgrade_level
    level_nhp = upgrade_level - level_hp
    if max_hp < upgrade_level:
        level_nhp = max_hp - level_hp
    
    return tiers[level + 1] * level_hp + tiers[nlevel + 1] * level_nhp + f' {hp}/{max_hp}' * number
    


class ConfirmButton(ui.View):
    def __init__(self):
        super().__init__()
    
    @ui.button(label="Ok", style=nextcord.ButtonStyle.blurple)
    async def ok(self, btn: ui.Button, interaction: Interaction):
        # Ok!
        # Does nothing.
        self.stop()
