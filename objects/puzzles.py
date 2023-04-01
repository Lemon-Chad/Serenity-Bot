from nextcord import Interaction
from objects.entities import DisCharacter
from abc import ABC, abstractmethod
from ui import puzzles


class Puzzle(ABC):
    player: DisCharacter
    
    def __init__(self, player: DisCharacter) -> None:
        super().__init__()
        self.player = player
    
    @abstractmethod
    async def main(self, interaction: Interaction) -> bool:
        ...


class MinePuzzle(Puzzle):
    def __init__(self, player: DisCharacter) -> None:
        super().__init__(player)

    async def main(self, interaction: Interaction) -> bool:
        msg = await interaction.send("** **", ephemeral=True)
        
        m_view = puzzles.MinePuzzleView(msg, interaction)
        await m_view.update()
        await m_view.wait()
        
        await msg.delete()
        return m_view.survived
