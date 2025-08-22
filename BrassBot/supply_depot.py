from .structure import Structure
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId

class SupplyDepot(Structure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
    
    async def on_step(self):
        await super().on_step()
        actual_supply_depot = self.get_self()
        if actual_supply_depot.type_id == UnitTypeId.SUPPLYDEPOT:
            actual_supply_depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER)