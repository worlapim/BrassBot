from .addonable_structure import AddonableStructure
from sc2.bot_ai import AbilityId, UnitTypeId

class Starport(AddonableStructure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
    
    async def on_step(self):
        actual_starport = self.get_self()
        await super().on_step()
        if self.has_idle_production():
            if self.bot.can_afford(UnitTypeId.TECHLAB) and not actual_starport.has_add_on and not self.bot.is_upol:
                self.build_tech_lab()
            elif actual_starport.has_add_on and self.bot.can_afford(UnitTypeId.RAVEN) and len(self.bot.units(UnitTypeId.RAVEN)) == 0 and not self.bot.is_upol:
                self.train_raven()
            elif (self.bot.can_afford(UnitTypeId.VIKINGFIGHTER) and len(self.bot.units(UnitTypeId.VIKINGFIGHTER)) + len(self.bot.units(UnitTypeId.VIKINGASSAULT)) <= 0) or (self.bot.enemy_info.is_doing_air and len(self.bot.units(UnitTypeId.MEDIVAC)) > 0):
                self.train_viking()
            elif self.bot.can_afford(UnitTypeId.MEDIVAC):
                self.train_medivac()

    def train_viking(self):
        if not self.bot.is_halt_spending:
            starport = self.get_self()
            starport.train(UnitTypeId.VIKINGFIGHTER)
    
    def train_medivac(self):
        if not self.bot.is_halt_spending:
            starport = self.get_self()
            starport.train(UnitTypeId.MEDIVAC)
    
    def train_liberator(self):
        if not self.bot.is_halt_spending:
            starport = self.get_self()
            starport.train(UnitTypeId.LIBERATOR)
    
    def train_banshee(self):
        if not self.bot.is_halt_spending:
            starport = self.get_self()
            starport.train(UnitTypeId.BANSHEE)
    
    def train_raven(self):
        if not self.bot.is_halt_spending:
            starport = self.get_self()
            starport.train(UnitTypeId.RAVEN)
    
    def train_battlecruiser(self):
        if not self.bot.is_halt_spending:
            starport = self.get_self()
            starport.train(UnitTypeId.BATTLECRUISER)

    def research_banshee_cloaking(self):
        if not self.bot.is_halt_spending and self.has_techlab:
            self.addon(AbilityId.RESEARCH_BANSHEECLOAKINGFIELD)