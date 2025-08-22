from .structure import Structure

class Bunker(Structure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
    
    async def on_step(self):
        await super().on_step()