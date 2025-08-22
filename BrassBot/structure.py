from .tasks import Task
from .structure_or_unit import StructureOrUnit

class Structure(StructureOrUnit):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
        self.can_autoattack = False

    async def on_step(self):
        await super().on_step()

    async def on_before_step(self):
        await super().on_before_step()

    async def on_after_step(self):
        await super().on_after_step()

    def update_self(self):
        actual_unit = (self.bot.structures).filter(lambda unit : unit.tag == self.tag)
        if len(actual_unit) > 0:
            self.actual_unit = actual_unit[0]
            self.time_not_updated_actual_unit = 0
        else:
            self.time_not_updated_actual_unit += 1
        self.is_active = not self.get_self().is_memory
    
    def has_idle_production(self) -> bool:
        return len(self.get_self().orders) < 1

    # def get_self(self):
    #     actual_structures = self.bot.structures.filter(lambda structures : structures.tag == self.tag)
    #     if len(actual_structures) > 0:
    #         return actual_structures[0]