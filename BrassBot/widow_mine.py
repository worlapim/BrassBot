from .unit import Unit

class WidowMine(Unit):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
        self.can_autoattack = False
    
    async def on_step(self):
        await super().on_step()