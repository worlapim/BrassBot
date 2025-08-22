from .worker import Worker
from .tasks import Task
from sc2.ids.unit_typeid import UnitTypeId

class Scv(Worker):
    
    async def on_step(self):
        await super().on_step()

    async def on_building_construction_complete(self, unit):
        await super().on_building_construction_complete(unit)
        if self.task == Task.BUILDING:
            is_location = False
            if self.building_structure == UnitTypeId.REFINERY:
                is_location = unit.get_self().distance_to(self.building_position.position) < 1
            else:
                is_location = unit.get_self().distance_to(self.building_position) < 1
            if unit.get_self().type_id == self.building_structure and is_location:
                self.building_position = None
                self.building_structure = None
                if unit.get_self().type_id == UnitTypeId.REFINERY:
                    self.task = Task.GASS_MINING
                    self.mine = None
                    self.vespene_mine = unit
                else:
                    self.task = Task.MINING

