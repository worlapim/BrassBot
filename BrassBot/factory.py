from .addonable_structure import AddonableStructure
from sc2.bot_ai import AbilityId, UnitTypeId

class Factory(AddonableStructure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
    
    async def on_step(self):
        await super().on_step()

    async def on_step(self):
        actual_factory = self.get_self()
        await super().on_step()
        if self.has_idle_production():
            if self.bot.can_afford(UnitTypeId.TECHLAB) and not actual_factory.has_add_on and (self.bot.strat.spam_helions or self.bot.strat.thors):
                self.build_tech_lab()
            elif self.bot.can_afford(UnitTypeId.THOR) and self.bot.strat.thors and actual_factory.has_add_on and self.bot.structures(UnitTypeId.ARMORY).ready.amount:
                self.train_thor()
            elif self.bot.can_afford(UnitTypeId.HELLION) and self.bot.strat.spam_helions:
                self.train_hellion()
    
    def train_hellion(self):
        if not self.bot.is_halt_spending:
            factory = self.get_self()
            factory.train(UnitTypeId.HELLION)
            
    def train_hellbat(self):
        if not self.bot.is_halt_spending:
            factory = self.get_self()
            factory.train(UnitTypeId.HELLIONTANK)
    
    def train_widow_mine(self):
        if not self.bot.is_halt_spending:
            factory = self.get_self()
            factory.train(UnitTypeId.WIDOWMINE)
    
    
    def train_siege_tank(self):
        if not self.bot.is_halt_spending:
            factory = self.get_self()
            factory.train(UnitTypeId.SIEGETANK)
    
    def train_cyclone(self):
        if not self.bot.is_halt_spending:
            factory = self.get_self()
            factory.train(UnitTypeId.CYCLONE)
    
    def train_thor(self):
        if not self.bot.is_halt_spending:
            factory = self.get_self()
            factory.train(UnitTypeId.THOR)
    
    def research_blue_flame(self):
        if not self.bot.is_halt_spending and self.has_techlab:
            self.addon(AbilityId.RESEARCH_INFERNALPREIGNITER)
            #self.bot.macro.blueflame_pending = True
    
    def research_drilling_claws(self):
        if not self.bot.is_halt_spending and self.has_techlab:
            self.addon(AbilityId.RESEARCH_DRILLINGCLAWS)
    
    def research_mag_field_accelerator(self):#Mag-Field Accelerator mi nešlo najít v enumech
        if not self.bot.is_halt_spending and self.has_techlab:
        #    self.addon(AbilityId.RESEARCH_DRILLINGCLAWS)
            pass
    
    def research_smart_servos(self):
        if not self.bot.is_halt_spending and self.has_techlab:
            # print(await self.bot.get_available_abilities(self.get_self()))
            # print(await self.bot.get_available_abilities(self.addon))
            self.addon(AbilityId.RESEARCH_SMARTSERVOS)