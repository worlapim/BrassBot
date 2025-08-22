from .unit import Unit

class Banshee(Unit):
    
    async def on_step(self):
        await super().on_step()