from .structure import Structure
from sc2.bot_ai import AbilityId, UnitTypeId

class EnergeeringBay(Structure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
    
    async def on_step(self):
        await super().on_step()

    def research_infantry_weapons1(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1)

    def research_infantry_weapons2(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2)

    def research_infantry_weapons3(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3)

    def research_infantry_armor1(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1)

    def research_infantry_armor2(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2)

    def research_infantry_armor3(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3)

    def research_hisec_autotracking(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.RESEARCH_HISECAUTOTRACKING)

    def research_building_armor(self): #asi nefunguje
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.RESEARCH_NEOSTEELFRAME)