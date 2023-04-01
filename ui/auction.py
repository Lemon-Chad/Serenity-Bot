import nextcord
from nextcord import Interaction
from nextcord import ui


# TODO: This.
class AuctionView(ui.View):
    def __init__(self) -> None:
        super().__init__()
