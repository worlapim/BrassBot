from .structure import Structure
from sc2.position import Point2
from sc2.bot_ai import AbilityId, UnitTypeId

class AddonableStructure(Structure):
    techlabIds = [UnitTypeId.TECHLAB, UnitTypeId.BARRACKSTECHLAB, UnitTypeId.FACTORYTECHLAB, UnitTypeId.STARPORTTECHLAB]
    reactorIds = [UnitTypeId.REACTOR, UnitTypeId.BARRACKSREACTOR, UnitTypeId.FACTORYREACTOR, UnitTypeId.STARPORTREACTOR]
    addonIds = techlabIds + reactorIds

    def __init__(self, bot, tag):
        self.addon = None
        self.has_addon = False
        self.has_reactor = False
        self.has_techlab = False
        self.has_techlab_idle = False
        super().__init__(bot, tag)
    
    async def on_step(self):
        await super().on_step()
    
    def update_self(self):
        super().update_self()
        self.addon = None
        self.has_addon = False
        self.has_reactor = False
        self.has_techlab = False
        self.has_techlab_idle = False
        actual_structure = self.get_self()
        if actual_structure and not (actual_structure.type_id == UnitTypeId.BARRACKSFLYING or actual_structure.type_id == UnitTypeId.FACTORYFLYING or actual_structure.type_id == UnitTypeId.STARPORTFLYING):
            addons = self.bot.structures.filter(lambda structure : structure.type_id in self.addonIds).closer_than(0.5, actual_structure.position + self.bot.geometry.addon_offset)
            if addons != []:
                self.addon = addons[0]
                self.has_addon = True
                self.has_reactor = self.addon.type_id in self.reactorIds
                self.has_techlab = self.addon.type_id in self.techlabIds
                if self.has_techlab:
                    self.has_techlab_idle = self.addon.is_idle
    
    
    def has_idle_production(self) -> bool:
        if self.has_reactor:
            return len(self.get_self().orders) < 2
        return super().has_idle_production()

    def build_tech_lab(self):
        if not self.bot.is_halt_spending:
            from .barrack import Baracks
            from .factory import Factory
            from .starport import Starport
            actual_structure = self.get_self()
            if type(self) == Baracks:
                actual_structure(AbilityId.BUILD_TECHLAB_BARRACKS)
            if type(self) == Factory:
                actual_structure(AbilityId.BUILD_TECHLAB_FACTORY)
            if type(self) == Starport:
                actual_structure(AbilityId.BUILD_TECHLAB_STARPORT)

    def build_reactor(self):
        if not self.bot.is_halt_spending:
            from .barrack import Baracks
            from .factory import Factory
            from .starport import Starport
            actual_structure = self.get_self()
            if type(self) == Baracks:
                actual_structure(AbilityId.BUILD_REACTOR_BARRACKS)
            if type(self) == Factory:
                actual_structure(AbilityId.BUILD_REACTOR_FACTORY)
            if type(self) == Starport:
                actual_structure(AbilityId.BUILD_REACTOR_STARPORT)
    
    def research(self, research):
        if not self.bot.is_halt_spending and self.has_techlab:
            self.addon(research)