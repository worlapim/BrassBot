from .unit import Unit
from sc2.ids.ability_id import AbilityId

class Thor(Unit):
    
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
        self.is_high_impact_mode = False
    
    async def on_before_step(self):
        await super().on_before_step()
        if AbilityId.MORPH_THORHIGHIMPACTMODE in self.abilities:
            self.is_high_impact_mode = False
        else:
            self.is_high_impact_mode = True
        self.form_and_copy_task_from_parent()
    
    async def on_step(self):
        if self.is_high_impact_mode and len(self.get_targets_for_high_impact_mode()) == 0 and len(self.get_targets_for_explosive_mode()) > 0:
            self.explosive_mode()
        elif not self.is_high_impact_mode and len(self.get_targets_for_explosive_mode()) == 0 and len(self.get_targets_for_high_impact_mode()) > 0:
            self.high_impact_mode()
        else:
            await super().on_step()

    def high_impact_mode(self):
        actual_unit = self.get_self()
        if AbilityId.MORPH_THORHIGHIMPACTMODE in self.abilities:
            actual_unit(AbilityId.MORPH_THORHIGHIMPACTMODE)
            self.is_high_impact_mode = True

    def explosive_mode(self):
        actual_unit = self.get_self()
        if AbilityId.MORPH_THOREXPLOSIVEMODE in self.abilities:
            actual_unit(AbilityId.MORPH_THOREXPLOSIVEMODE)
            self.is_high_impact_mode = False
    
    def get_targets_for_high_impact_mode(self, bonus_range = 0):
        return self.bot.enemy_units.flying().filter(lambda enemy : enemy.is_massive).closer_than(11 + bonus_range + self.get_self().radius, self.get_self().position)

    def get_targets_for_explosive_mode(self, bonus_range = 0):
        return self.bot.enemy_units.flying().filter(lambda enemy : enemy.is_light).closer_than(10 + bonus_range + self.get_self().radius, self.get_self().position)