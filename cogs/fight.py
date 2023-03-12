import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from events.battle import Battle
from objects import items
from objects.entities import DisCharacter, Enemy, generate_stats


TESTING_GUILDS = [658882526470864896, 811033467139784734, 1082795791476858980]


class Fight(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client: commands.Bot):
    client.add_cog(Fight(client))
