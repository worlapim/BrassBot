from .addonable_structure import AddonableStructure

from sc2.bot_ai import AbilityId, UnitTypeId


class Baracks(AddonableStructure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
    
    async def on_step(self):
        actual_barracks = self.get_self()
        wait_for_ghost = self.bot.strat.ghosts and len(self.bot.structures(UnitTypeId.GHOSTACADEMY).ready) >= 1 and len(self.bot.units(UnitTypeId.GHOST)) == 0 and self.bot.minerals < 150 and actual_barracks.has_techlab
        await super().on_step()
        if self.has_idle_production():
            if self.bot.can_afford(UnitTypeId.REAPER) and len(self.bot.units(UnitTypeId.REAPER)) == 0 and self.bot.strat.reapers and not wait_for_ghost:
                self.train_reaper()
            elif self.bot.can_afford(UnitTypeId.TECHLAB) and not actual_barracks.has_add_on and not self.bot.enemy_info.is_doing_air:
                self.build_tech_lab()
            elif self.bot.can_afford(UnitTypeId.REACTOR) and not actual_barracks.has_add_on and self.bot.enemy_info.is_doing_air:
                self.build_reactor()
            elif self.bot.can_afford(UnitTypeId.GHOST) and self.bot.structures(UnitTypeId.GHOSTACADEMY).ready and self.bot.strat.ghosts and actual_barracks.has_techlab:
                self.train_ghost()
            elif self.bot.can_afford(UnitTypeId.MARAUDER) and actual_barracks.has_techlab and not wait_for_ghost and not self.bot.enemy_info.is_doing_air:
                self.train_marauder()
            elif self.bot.can_afford(UnitTypeId.MARINE) and not wait_for_ghost:
                self.train_marine()
    
    def train_marine(self):
        if not self.bot.is_halt_spending:
            self.get_self().train(UnitTypeId.MARINE)
    
    def train_marauder(self):
        if not self.bot.is_halt_spending:
            self.get_self().train(UnitTypeId.MARAUDER)
    
    def train_reaper(self):
        if not self.bot.is_halt_spending:
            self.get_self().train(UnitTypeId.REAPER)
    
    def train_ghost(self):
        if not self.bot.is_halt_spending:
            self.get_self().train(UnitTypeId.GHOST)
    
    def research_combat_shield(self):
        if not self.bot.is_halt_spending and self.has_techlab:
            self.addon(AbilityId.RESEARCH_COMBATSHIELD)
            #self.bot.macro.combatshield_pending = True
    
    def research_stimpack(self):
        if not self.bot.is_halt_spending and self.has_techlab:
            self.addon(AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK)
    
    def research_concusive_shell(self):
        if not self.bot.is_halt_spending and self.has_techlab:
            self.addon(AbilityId.RESEARCH_CONCUSSIVESHELLS)
            #self.bot.macro.concusiveshells_pending = True