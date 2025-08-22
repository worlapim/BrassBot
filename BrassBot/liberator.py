from .unit import Unit

class Liberator(Unit):
    
    async def on_step(self):
        await super().on_step()