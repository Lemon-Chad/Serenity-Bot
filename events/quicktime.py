from nextcord import ui
import nextcord
import random


class QuicktimeEvent(ui.View):
    def __init__(self, speed: int, 
                 correct_style: int, incorrect_style: int, 
                 correct_emoji: str, incorrect_emoji: str,
                 option_count: int, correct_chance: float, always_possible: bool):
        super().__init__(timeout=speed)
        
        self.success = False
        self.clicked = False
        self.correct_indices = [ i for i in range(0, option_count) if random.random() < correct_chance ]
        if not self.correct_indices and always_possible:
            self.correct_indices = [ random.randint(0, option_count - 1) ]
        
        for i in range(option_count):
            btn = ui.Button()
            
            if i in self.correct_indices:
                btn.style = correct_style
                btn.emoji = correct_emoji
            else:
                btn.style = incorrect_style
                btn.emoji = incorrect_emoji
                
            btn.callback = self.build_try_event(i)
            
            self.children.append(btn)
    
    def build_try_event(self, index: int):
        async def anon(_interaction):
            await self.try_event(index)
        return anon
    
    async def try_event(self, index: int):
        self.success = index in self.correct_indices
        self.clicked = True
        self.stop()
        
    async def close(self, message: nextcord.Message):
        self.children = []
        await message.edit(view=self)
