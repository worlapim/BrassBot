from .unit import Unit

class Mule(Unit):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
        self.can_autoattack = False
    
    async def on_step(self):
        pass