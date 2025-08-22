from .unit import Unit

class Viking(Unit):
    
    async def on_step(self):
        await super().on_step()
        self.form_and_copy_task_from_parent()