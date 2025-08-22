from .structure import Structure
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from .option import Option, chose_option

class BaseStructure(Structure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)

    async def on_step(self):
        actual_base = self.get_self()
        await super().on_step()
        if type(actual_base) == UnitTypeId.COMMANDCENTER and actual_base.energy >= 50:
            self.mining_mule()

    def train_scv(self):
        if not self.bot.is_halt_spending:
            actual_base_structure = self.get_self()
            actual_base_structure.train(UnitTypeId.SCV)

    def become_orbital(self):
        if not self.bot.is_halt_spending:
            actual_base_structure = self.get_self()
            actual_base_structure(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)

    def become_planetary(self):
        if not self.bot.is_halt_spending:
            actual_base_structure = self.get_self()
            actual_base_structure(AbilityId.UPGRADETOPLANETARYFORTRESS_PLANETARYFORTRESS)
    
    def mining_mule(self):
        mineral_fields = self.bot.mineral_field
        options = []
        for mineral_field in mineral_fields:
            position = mineral_field.position
            motivation = mineral_field.mineral_contents * len(self.bot.structures(UnitTypeId.COMMANDCENTER).closer_than(8,position).ready + self.bot.structures(UnitTypeId.ORBITALCOMMAND).closer_than(8,position).ready + self.bot.structures(UnitTypeId.PLANETARYFORTRESS).closer_than(8,position).ready)
            options.append(Option(self.bot, motivation, mineral_field))
        if options != []:
            mineral_field = chose_option(options).what
            actual_base_structure = self.get_self()
            if actual_base_structure.type_id == UnitTypeId.ORBITALCOMMAND:
                actual_base_structure(AbilityId.CALLDOWNMULE_CALLDOWNMULE, mineral_field)
