from .unit import Unit

class Battlecruiser(Unit):
    
    async def on_step(self):
        await super().on_step()