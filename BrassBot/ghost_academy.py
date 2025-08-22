from .structure import Structure
from sc2.bot_ai import AbilityId, UnitTypeId

class GhostAcademy(Structure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
    
    async def on_step(self):
        await super().on_step()
        if AbilityId.BUILD_NUKE in self.abilities and self.get_self().is_idle:
            self.build_nuke()

    def research_enhanced_shockwaves(self):#možná nefunguje
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.GHOSTACADEMYRESEARCH_RESEARCHENHANCEDSHOCKWAVES)

    def build_nuke(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.BUILD_NUKE)

    def research_personal_cloaking(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.RESEARCH_PERSONALCLOAKING)