from .unit import Unit
from .stimable_unit import StimableUnit
from sc2.ids.ability_id import AbilityId

class Marauder(StimableUnit):
    
    async def on_step(self):
        await super().on_step()
        self.form_and_copy_task_from_parent()
    
    def stim(self):
        self.get_self()(AbilityId.EFFECT_STIM_MARAUDER)