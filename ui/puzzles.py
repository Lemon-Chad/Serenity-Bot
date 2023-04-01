import nextcord
from nextcord import Interaction, ui
from typing import List
from objects.entities import DisCharacter
import random

class MinePuzzleView(ui.View):
    player: DisCharacter
    interaction: Interaction
    msg: nextcord.Message
    board: List[int]
    marked: List[bool]
    survived: bool

    NUMBERS = ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']

    def __init__(self, message: nextcord.Message, interaction: Interaction) -> None:
        super().__init__()

        self.interaction = interaction
        self.msg = message
        self.survived = False

        self.w, self.h = 5, 5
        self.mines = 5
        self.max_lives = 3
        self.lives = self.max_lives

        open_spaces = [ (x, y) for x in range(self.w) for y in range(self.h) ]
        self.board = [ 0 for _ in open_spaces ]
        self.marked = [ False for _ in self.board ]
        for _ in range(self.mines):
            x, y = random.choice(open_spaces)
            open_spaces.remove((x, y))
            self.set_spot(x, y, -10000)
            for x1 in range(-1, 2):
                for y1 in range(-1, 2):
                    self.set_spot(x + x1, y + y1, 1)
        for _ in range(self.mines):
            x, y = random.choice(open_spaces)
            open_spaces.remove((x, y))
            self.marked[x + y * self.w] = True

    async def update(self):
        self.clear_items()

        for y in range(self.h):
            for x in range(self.w):
                i = x + y * self.w
                button = ui.Button(row=y)
                if self.marked[i]:
                    if self.board[i] >= 0:
                        button.emoji = MinePuzzleView.NUMBERS[self.board[i]]
                        button.style = nextcord.ButtonStyle.grey
                    else:
                        button.emoji = '💣'
                        button.style = nextcord.ButtonStyle.red
                else:
                    button.label = "\u200b"
                    button.style = nextcord.ButtonStyle.blurple
                    button.callback = self.click_builder(i)
                self.add_item(button)

        embed = nextcord.Embed(
            title="Minefield Puzzle",
            description='❤️' * self.lives + '🖤' * (self.max_lives - self.lives),
            color=0xf1c40f,
        )
        
        await self.msg.edit(view=self, embed=embed)

    def click_builder(self, space):
        async def anon(_: Interaction):
            await self.inspect_spot(space)
        return anon

    async def inspect_spot(self, space):
        self.marked[space] = True
        if self.board[space] < 0:
            self.lives -= 1
            if self.lives <= 0:
                self.stop()
        else:
            if len([ x for x in self.marked if not x ]) == self.mines:
                self.survived = True
                self.stop()
        await self.update()
    
    def set_spot(self, x, y, v, add=True):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return
        i = x + y * self.w
        if add:
            self.board[i] += v
        else:
            self.board[i] = v
