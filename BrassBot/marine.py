from .unit import Unit
from .tasks import Task
from .stimable_unit import StimableUnit
from sc2.ids.ability_id import AbilityId

class Marine(StimableUnit):

    async def on_before_step(self):
        await super().on_before_step()
        self.form_and_copy_task_from_parent()
        actual_self = self.get_self()
        if actual_self.shield_health_percentage < 0.5 and self.get_threats(3):
            self.task = Task.ATTACKING_CAREFULLY

    async def on_after_step(self):
        await super().on_after_step()
    
    async def on_step(self):
        await super().on_step()

    def stim(self):
        self.get_self()(AbilityId.EFFECT_STIM_MARINE)