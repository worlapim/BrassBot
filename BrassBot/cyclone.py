from .unit import Unit

class Cyclone(Unit):
    
    async def on_step(self):
        await super().on_step()