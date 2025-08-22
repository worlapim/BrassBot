from .structure import Structure

class Refinery(Structure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
        self.vespene_contents = self.get_self().vespene_contents
    
    async def on_step(self):
        await super().on_step()
        self.vespene_contents = self.get_self().vespene_contents
