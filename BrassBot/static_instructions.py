from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.effect_id import EffectId

class StaticInstructions():
    def __init__(self,bot):
        self.bot = bot
        self.detectors = {UnitTypeId.OBSERVER, UnitTypeId.RAVEN, UnitTypeId.OVERSEER, UnitTypeId.MISSILETURRET, UnitTypeId.SPORECRAWLER, UnitTypeId.PHOTONCANNON, UnitTypeId.ORACLE, UnitTypeId.GHOST}
        self.snipe_worthy = {UnitTypeId.GHOST, UnitTypeId.RAVEN, UnitTypeId.SIEGETANK, UnitTypeId.SIEGETANKSIEGED, UnitTypeId.CYCLONE, UnitTypeId.THOR, UnitTypeId.BATTLECRUISER, UnitTypeId.LIBERATOR, UnitTypeId.MEDIVAC, UnitTypeId.BANSHEE,
                             UnitTypeId.BANELING, UnitTypeId.RAVAGER, UnitTypeId.INFESTOR, UnitTypeId.BROODLORD, UnitTypeId.ULTRALISK, UnitTypeId.QUEEN, UnitTypeId.MUTALISK,
                             UnitTypeId.BANELINGBURROWED, UnitTypeId.RAVAGERBURROWED, UnitTypeId.INFESTORBURROWED, UnitTypeId.ULTRALISKBURROWED, UnitTypeId.QUEENBURROWED,
                             UnitTypeId.HIGHTEMPLAR, UnitTypeId.DARKTEMPLAR, UnitTypeId.ARCHON, UnitTypeId.DISRUPTOR, UnitTypeId.STALKER, UnitTypeId.VOIDRAY, UnitTypeId.ORACLE, UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS, UnitTypeId.PHOENIX, UnitTypeId.MOTHERSHIP, UnitTypeId.CARRIER, UnitTypeId.TEMPEST, UnitTypeId.SENTRY}
        self.area_effects = {AreaEffectStaticInfo(EffectId.NUKEPERSISTENT, 13), AreaEffectStaticInfo(EffectId.RAVAGERCORROSIVEBILECP, 1), AreaEffectStaticInfo(EffectId.PSISTORMPERSISTENT, 5)}
        self.nonthreatening_air_units = {UnitTypeId.OVERLORD, UnitTypeId.OVERLORDTRANSPORT, UnitTypeId.OVERSEER, UnitTypeId.OBSERVER}
        self.changeling_types = {UnitTypeId.CHANGELING, UnitTypeId.CHANGELINGMARINE, UnitTypeId.CHANGELINGMARINESHIELD, UnitTypeId.CHANGELINGZEALOT, UnitTypeId.CHANGELINGZERGLING, UnitTypeId.CHANGELINGZERGLINGWINGS}
        self.target_priority_rating = {UnitTargetPriorityRating(UnitTypeId.SCV, 30), UnitTargetPriorityRating(UnitTypeId.DRONE, 30), UnitTargetPriorityRating(UnitTypeId.PROBE, 30), UnitTargetPriorityRating(UnitTypeId.MULE, 25),
                                       
                                       UnitTargetPriorityRating(UnitTypeId.MARINE, 50), UnitTargetPriorityRating(UnitTypeId.MARAUDER, 40), UnitTargetPriorityRating(UnitTypeId.REAPER, 60), UnitTargetPriorityRating(UnitTypeId.GHOST, 100), 
                                       UnitTargetPriorityRating(UnitTypeId.HELLION, 45), UnitTargetPriorityRating(UnitTypeId.HELLIONTANK, 50), UnitTargetPriorityRating(UnitTypeId.CYCLONE, 50), UnitTargetPriorityRating(UnitTypeId.SIEGETANK, 70), 
                                       UnitTargetPriorityRating(UnitTypeId.SIEGETANKSIEGED, 90), UnitTargetPriorityRating(UnitTypeId.WIDOWMINE, 75), UnitTargetPriorityRating(UnitTypeId.WIDOWMINEBURROWED, 75), UnitTargetPriorityRating(UnitTypeId.THOR, 55), 
                                       UnitTargetPriorityRating(UnitTypeId.VIKINGASSAULT, 40), UnitTargetPriorityRating(UnitTypeId.VIKINGFIGHTER, 40), UnitTargetPriorityRating(UnitTypeId.MEDIVAC, 55), UnitTargetPriorityRating(UnitTypeId.LIBERATOR, 70), 
                                       UnitTargetPriorityRating(UnitTypeId.RAVEN, 65), UnitTargetPriorityRating(UnitTypeId.BANSHEE, 80), UnitTargetPriorityRating(UnitTypeId.BATTLECRUISER, 75),   

                                       UnitTargetPriorityRating(UnitTypeId.ZERGLING, 65), UnitTargetPriorityRating(UnitTypeId.BANELING, 100), UnitTargetPriorityRating(UnitTypeId.ROACH, 45), UnitTargetPriorityRating(UnitTypeId.HYDRALISK, 50), 
                                       UnitTargetPriorityRating(UnitTypeId.RAVAGER, 55), UnitTargetPriorityRating(UnitTypeId.LURKER, 75), UnitTargetPriorityRating(UnitTypeId.LURKERBURROWED, 85), UnitTargetPriorityRating(UnitTypeId.INFESTOR, 75), 
                                       UnitTargetPriorityRating(UnitTypeId.INFESTORBURROWED, 75), UnitTargetPriorityRating(UnitTypeId.ULTRALISK, 70), UnitTargetPriorityRating(UnitTypeId.MUTALISK, 55), UnitTargetPriorityRating(UnitTypeId.CORRUPTOR, 40), 
                                       UnitTargetPriorityRating(UnitTypeId.BROODLORD, 80), UnitTargetPriorityRating(UnitTypeId.BROODLING, 55), UnitTargetPriorityRating(UnitTypeId.SWARMHOSTMP, 65), UnitTargetPriorityRating(UnitTypeId.LOCUSTMP, 50), 
                                       UnitTargetPriorityRating(UnitTypeId.LOCUSTMPFLYING, 50), UnitTargetPriorityRating(UnitTypeId.QUEEN, 55), UnitTargetPriorityRating(UnitTypeId.VIPER, 65), UnitTargetPriorityRating(UnitTypeId.CHANGELING, 5), 
                                       UnitTargetPriorityRating(UnitTypeId.OVERLORD, 15), UnitTargetPriorityRating(UnitTypeId.OVERLORDTRANSPORT, 40), UnitTargetPriorityRating(UnitTypeId.OVERSEER, 35), 
                                       
                                       UnitTargetPriorityRating(UnitTypeId.ZEALOT, 65), UnitTargetPriorityRating(UnitTypeId.ADEPT, 50), UnitTargetPriorityRating(UnitTypeId.STALKER, 40), UnitTargetPriorityRating(UnitTypeId.SENTRY, 65), 
                                       UnitTargetPriorityRating(UnitTypeId.DARKTEMPLAR, 100), UnitTargetPriorityRating(UnitTypeId.HIGHTEMPLAR, 100), UnitTargetPriorityRating(UnitTypeId.ARCHON, 55), UnitTargetPriorityRating(UnitTypeId.IMMORTAL, 55), 
                                       UnitTargetPriorityRating(UnitTypeId.COLOSSUS, 70), UnitTargetPriorityRating(UnitTypeId.DISRUPTOR, 85), UnitTargetPriorityRating(UnitTypeId.VOIDRAY, 50), UnitTargetPriorityRating(UnitTypeId.ORACLE, 70), 
                                       UnitTargetPriorityRating(UnitTypeId.PHOENIX, 70), UnitTargetPriorityRating(UnitTypeId.CARRIER, 65), UnitTargetPriorityRating(UnitTypeId.INTERCEPTOR, 70), UnitTargetPriorityRating(UnitTypeId.TEMPEST, 70), 
                                       UnitTargetPriorityRating(UnitTypeId.WARPPRISM, 70), UnitTargetPriorityRating(UnitTypeId.WARPPRISMPHASING, 80), UnitTargetPriorityRating(UnitTypeId.OBSERVER, 45)}
        self.ignored_targets = {UnitTypeId.EGG, UnitTypeId.LARVA} | self.changeling_types

        
        
    def get_priority_rating_for_unit(self, unit) -> int:
        for rating in self.target_priority_rating:
            if rating.unit_id == unit.type_id:
                return rating.rating
        return 50

class UnitTargetPriorityRating():
    def __init__(self, unit_type_id, rating):
        self.unit_id = unit_type_id
        self.rating = rating

class AreaEffectStaticInfo():
    def __init__(self, unit_type_id, radius):
        self.effect_id = unit_type_id
        self.radius = radius