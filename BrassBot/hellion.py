from .unit import Unit
from .tasks import Task

class Hellion(Unit):

    async def on_before_step(self):
        await super().on_before_step()
        self.form_and_copy_task_from_parent()

    async def on_after_step(self):
        await super().on_after_step()
    
    async def on_step(self):
        await super().on_step()

    def do_attacking(self):
        actual_self = self.get_self()
        if actual_self.weapon_cooldown == 0:
            super().do_attacking()
        else:
            self.flee()
