from .structure import Structure
from sc2.bot_ai import AbilityId, UnitTypeId

class Armory(Structure):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
    
    async def on_step(self):
        await super().on_step()

    def research_vehicle_weapons1(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1)

    def research_vehicle_weapons2(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2)

    def research_vehicle_weapons3(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3)

    def research_vehicle_armor1(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1)

    def research_vehicle_armor2(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2)

    def research_vehicle_armor3(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3)

    def research_air_weapons1(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL1)

    def research_air_weapons2(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL2)

    def research_air_weapons3(self):
        if not self.bot.is_halt_spending:
            self.get_self()(AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL3)

    # def research_air_armor1(self):
    #     if not self.bot.is_halt_spending:
    #         self.get_self()(AbilityId.ARMORYRESEARCH_TERRANSHIPPLATINGLEVEL1)

    # def research_air_armor2(self):
    #     if not self.bot.is_halt_spending:
    #         self.get_self()(AbilityId.ARMORYRESEARCH_TERRANSHIPPLATINGLEVEL2)

    # def research_air_armor3(self):
    #     if not self.bot.is_halt_spending:
    #         self.get_self()(AbilityId.ARMORYRESEARCH_TERRANSHIPPLATINGLEVEL3)
        