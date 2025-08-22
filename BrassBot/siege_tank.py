from .unit import Unit

class SiegeTank(Unit):
    
    async def on_step(self):
        await super().on_step()