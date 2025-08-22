from sc2 import UnitTypeId, AbilityId
from .option import Option, chose_option, chose_lowest_option
from .building_line_group import BuildingLineWidth
from sc2.ids.upgrade_id import UpgradeId

class Macro():
    barracks_research = [UpgradeId.STIMPACK, UpgradeId.SHIELDWALL, UpgradeId.PUNISHERGRENADES]
    factory_research = [UpgradeId.HIGHCAPACITYBARRELS, UpgradeId.DRILLCLAWS, UpgradeId.SMARTSERVOS]
    starport_research = [UpgradeId.BANSHEECLOAK]
    armory_research =   [UpgradeId.TERRANVEHICLEWEAPONSLEVEL1,UpgradeId.TERRANVEHICLEWEAPONSLEVEL2,UpgradeId.TERRANVEHICLEWEAPONSLEVEL3,
                        UpgradeId.TERRANVEHICLEANDSHIPARMORSLEVEL1,UpgradeId.TERRANVEHICLEANDSHIPARMORSLEVEL2,UpgradeId.TERRANVEHICLEANDSHIPARMORSLEVEL3,
                        UpgradeId.TERRANSHIPWEAPONSLEVEL1,UpgradeId.TERRANSHIPWEAPONSLEVEL2,UpgradeId.TERRANSHIPWEAPONSLEVEL3]
    engennering_bay_research = [UpgradeId.TERRANINFANTRYWEAPONSLEVEL1,UpgradeId.TERRANINFANTRYWEAPONSLEVEL2,UpgradeId.TERRANINFANTRYWEAPONSLEVEL3,
                                UpgradeId.TERRANINFANTRYARMORSLEVEL1,UpgradeId.TERRANINFANTRYARMORSLEVEL2,UpgradeId.TERRANINFANTRYARMORSLEVEL3,
                                UpgradeId.NEOSTEELFRAME, UpgradeId.HISECAUTOTRACKING]

    ghost_academy_research = [UpgradeId.PERSONALCLOAKING]
    fusion_core_research = []
    research = barracks_research + factory_research + starport_research + engennering_bay_research + armory_research + ghost_academy_research + fusion_core_research

    upol_research = [UpgradeId.STIMPACK, UpgradeId.SHIELDWALL, UpgradeId.PUNISHERGRENADES,
                     UpgradeId.HIGHCAPACITYBARRELS,
                     UpgradeId.TERRANINFANTRYWEAPONSLEVEL1,UpgradeId.TERRANINFANTRYARMORSLEVEL1,
                     UpgradeId.NEOSTEELFRAME, UpgradeId.HISECAUTOTRACKING]

    combatshield_pending = False
    concusiveshells_pending = False
    blueflame_pending = False

    is_structure_at_enemy_spawn = True

    max_workers = 60

    def __init__(self,bot):
        self.bot = bot

    async def on_step(self):
        self.update_is_structure_at_enemy_spawn()
        self.reasign_workers_between_bases()
        if self.bot.townhalls.amount < (self.bot.time + 70) / 200 and self.get_amount_of_structure_pending(UnitTypeId.COMMANDCENTER) == 0:
            if self.bot.minerals < 400:
                self.bot.is_halt_spending = True
            else:
                self.bot.is_halt_spending = False
                await self.build(UnitTypeId.COMMANDCENTER)
        if self.bot.minerals >= 75 and self.bot.structures.filter(lambda structure : structure.type_id == UnitTypeId.REFINERY or 
                    structure.type_id == UnitTypeId.REFINERYRICH).amount + 1 < self.bot.time / 100 and self.get_amount_of_structure_pending(UnitTypeId.REFINERY) == 0 and self.bot.vespene < 200:
            await self.build(UnitTypeId.REFINERY)
        elif self.bot.supply_cap < 200 and self.bot.supply_left + 8 * self.get_amount_of_structure_pending(UnitTypeId.SUPPLYDEPOT) - 2 < self.bot.supply_cap / 8:
            if self.bot.can_afford(UnitTypeId.SUPPLYDEPOT):
                await self.build(UnitTypeId.SUPPLYDEPOT)
        else:
            if not self.bot.is_halt_spending:
                await self.decide_what_now()
            if self.bot.strat.tech_tree and not self.bot.is_halt_spending:
                await self.build_tree_progresion_structure()
            for research in self.research:
                if self.can_research(research) and self.should_research(research) and not self.bot.is_halt_spending:
                    self.do_research(research)
    
    def reasign_workers_between_bases(self):
        from .tasks import Task
        class BaseWorkerDistribution:
            base = None
            workers_missing = 0
        bases = []
        for group in self.bot.root_groups:
            from .base import Base
            if type(group) == Base:
                base_worker_distribution = BaseWorkerDistribution()
                base_worker_distribution.base = group
                base_worker_distribution.workers_missing = len(group.mineral_fields)*2 + len(group.refineries)*3 - len(group.workers)
                bases.append(base_worker_distribution)
        if len(bases) > 1:
            bases.sort(key= lambda base: base.workers_missing)
            if bases[0].workers_missing < 0 and bases[-1].workers_missing > 0:
                worker_options = []
                for worker in bases[0].base.workers:
                    if worker.task == Task.MINING:
                        worker_options.append(Option(self.bot, 50, who= worker))
                    elif worker.task == Task.GASS_MINING:
                        worker_options.append(Option(self.bot, 10, who= worker))
                    elif worker.task == Task.FLEEING:
                        worker_options.append(Option(self.bot, 80, who= worker))
                    elif worker.task == Task.FLEEING_AND_GUNNING:
                        worker_options.append(Option(self.bot, 60, who= worker))
                    elif worker.task == Task.NOTHING:
                        worker_options.append(Option(self.bot, 100, who= worker))
                choice = chose_option(worker_options)
                if choice != None:
                    bases[0].base.workers.remove(choice.who)
                    bases[0].base.members.remove(choice.who)
                    bases[-1].base.workers.append(choice.who)
                    bases[-1].base.members.append(choice.who)
                    choice.who.parent = bases[-1].base
                    bases[0].base.reasign_workers()
                    bases[-1].base.reasign_workers()


    def do_research(self, research):
            structure = self.get_structure_for_research(research, True)
            if research == UpgradeId.STIMPACK:
                structure.research_stimpack()
            if research == UpgradeId.SHIELDWALL:
                structure.research_combat_shield()
            if research == UpgradeId.PUNISHERGRENADES:
                structure.research_concusive_shell()
            if research == UpgradeId.HIGHCAPACITYBARRELS:
                structure.research_blue_flame()
            if research == UpgradeId.DRILLCLAWS:
                structure.research_drilling_claws()
            if research == UpgradeId.SMARTSERVOS:
                structure.research_smart_servos()
            if research == UpgradeId.BANSHEECLOAK:
                structure.research_banshee_cloaking()
            if research == UpgradeId.TERRANVEHICLEWEAPONSLEVEL1:
                structure.research_vehicle_weapons1()
            if research == UpgradeId.TERRANVEHICLEWEAPONSLEVEL2:
                structure.research_vehicle_weapons2()
            if research == UpgradeId.TERRANVEHICLEWEAPONSLEVEL3:
                structure.research_vehicle_weapons3()
            if research == UpgradeId.TERRANVEHICLEANDSHIPARMORSLEVEL1:
                structure.research_vehicle_armor1()
            if research == UpgradeId.TERRANVEHICLEANDSHIPARMORSLEVEL2:
                structure.research_vehicle_armor2()
            if research == UpgradeId.TERRANVEHICLEANDSHIPARMORSLEVEL3:
                structure.research_vehicle_armor3()
            if research == UpgradeId.TERRANSHIPWEAPONSLEVEL1:
                structure.research_air_weapons1()
            if research == UpgradeId.TERRANSHIPWEAPONSLEVEL2:
                structure.research_air_weapons2()
            if research == UpgradeId.TERRANSHIPWEAPONSLEVEL3:
                structure.research_air_weapons3()
            if research == UpgradeId.TERRANINFANTRYWEAPONSLEVEL1:
                structure.research_infantry_weapons1()
            if research == UpgradeId.TERRANINFANTRYWEAPONSLEVEL2:
                structure.research_infantry_weapons2()
            if research == UpgradeId.TERRANINFANTRYWEAPONSLEVEL3:
                structure.research_infantry_weapons3()
            if research == UpgradeId.TERRANINFANTRYARMORSLEVEL1:
                structure.research_infantry_armor1()
            if research == UpgradeId.TERRANINFANTRYARMORSLEVEL2:
                structure.research_infantry_armor2()
            if research == UpgradeId.TERRANINFANTRYARMORSLEVEL3:
                structure.research_infantry_armor3()
            if research == UpgradeId.NEOSTEELFRAME:
                structure.research_building_armor()
            if research == UpgradeId.HISECAUTOTRACKING:
                structure.research_hisec_autotracking()
            if research == UpgradeId.PERSONALCLOAKING:
                structure.research_personal_cloaking()

    def should_research(self, research) -> bool:
        if self.bot.strat.tech_tree:
            return True
        if self.bot.strat.spam_helions and (research == UpgradeId.HIGHCAPACITYBARRELS or research in self.armory_research):
            return True
        if self.bot.strat.ghosts and research == UpgradeId.PERSONALCLOAKING:
            return True
        if research in self.barracks_research + self.engennering_bay_research and research != UpgradeId.PUNISHERGRENADES:
            return True
        if research in self.armory_research and (self.bot.strat.spam_helions or self.bot.strat.thors):
            return True
        if research == UpgradeId.PUNISHERGRENADES and self.bot.already_pending_upgrade(UpgradeId.SHIELDWALL) != 0 and self.bot.already_pending_upgrade(UpgradeId.STIMPACK) != 0:
            return True
        return False

    def can_research(self, research) -> bool:
        if self.bot.is_upol and research not in self.upol_research:
            return False
        # if research == UpgradeId.SHIELDWALL:
        #     return self.bot.minerals >= 100 and self.bot.vespene >= 100 and self.bot.already_pending_upgrade(research) and self.get_structure_for_research(research, True)
        # if research == UpgradeId.PUNISHERGRENADES:
        #     return self.bot.minerals >= 50 and self.bot.vespene >= 50 and self.bot.already_pending_upgrade(research) and self.get_structure_for_research(research, True)
        # if research == UpgradeId.INFERNALPREIGNITERS:
        #      return self.bot.minerals >= 100 and self.bot.vespene >= 100 and self.get_structure_for_research(research, True)
        return self.bot.already_pending_upgrade(research) == 0 and self.bot.can_afford(research) and self.get_structure_for_research(research, True)
    
    def get_structure_for_research(self, research, can_be_non_idle):
        for structure in self.bot.frendly_structures_or_units:
            from .barrack import Baracks
            if research in self.barracks_research and type(structure) == Baracks:
                if (structure.has_techlab_idle) or (structure.has_techlab and not can_be_non_idle):
                    return structure
            from .factory import Factory
            if research in self.factory_research and type(structure) == Factory:
                if (structure.has_techlab_idle) or (structure.has_techlab and not can_be_non_idle):
                    return structure
            from .starport import Starport
            if research in self.starport_research and type(structure) == Starport:
                if (structure.has_techlab_idle) or (structure.has_techlab and not can_be_non_idle):
                    return structure
            from .armory import Armory
            if research in self.armory_research and type(structure) == Armory:
                if (structure.get_self().is_idle or not can_be_non_idle):
                    return structure
            from .engeneering_bay import EnergeeringBay
            if research in self.engennering_bay_research and type(structure) == EnergeeringBay:
                if (structure.get_self().is_idle or not can_be_non_idle):
                    return structure
            from .ghost_academy import GhostAcademy
            if research in self.ghost_academy_research and type(structure) == GhostAcademy:
                if (structure.get_self().is_idle or not can_be_non_idle):
                    return structure

        return None
    
    async def decide_what_now(self):
        if self.bot.structures(UnitTypeId.FACTORY).amount < 1 and self.bot.can_afford(UnitTypeId.FACTORY) and self.bot.tech_requirement_progress(UnitTypeId.FACTORY) == 1 and (not self.bot.strat.ghosts or self.bot.time >= 360):
            await self.build(UnitTypeId.FACTORY)
        if self.bot.structures(UnitTypeId.STARPORT).amount < 1 and self.bot.can_afford(UnitTypeId.STARPORT) and self.bot.tech_requirement_progress(UnitTypeId.STARPORT) == 1:
            await self.build(UnitTypeId.STARPORT)
        if self.bot.structures(UnitTypeId.BARRACKS).amount < 2 and self.bot.can_afford(UnitTypeId.BARRACKS) and self.bot.tech_requirement_progress(UnitTypeId.BARRACKS) == 1:
            await self.build(UnitTypeId.BARRACKS)
        if self.bot.structures(UnitTypeId.ENGINEERINGBAY).amount < 1 and self.bot.townhalls.same_tech({UnitTypeId.COMMANDCENTER}).amount >= 2 and self.bot.can_afford(UnitTypeId.ENGINEERINGBAY) and self.bot.tech_requirement_progress(UnitTypeId.ENGINEERINGBAY) == 1 and self.get_amount_of_structure_pending(UnitTypeId.ENGINEERINGBAY) == 0 and (not self.bot.strat.ghosts or self.bot.time >= 300):
            await self.build(UnitTypeId.ENGINEERINGBAY)
        if self.bot.structures(UnitTypeId.REFINERY).amount < 1 and self.bot.structures(UnitTypeId.BARRACKS).amount >= 1 and self.bot.can_afford(UnitTypeId.REFINERY) and self.bot.tech_requirement_progress(UnitTypeId.REFINERY) == 1:
            await self.build(UnitTypeId.REFINERY)
        if self.bot.structures(UnitTypeId.GHOSTACADEMY).amount < 1 and self.bot.structures(UnitTypeId.BARRACKS).amount >= 2 and self.bot.can_afford(UnitTypeId.GHOSTACADEMY) and self.bot.tech_requirement_progress(UnitTypeId.GHOSTACADEMY) == 1 and self.bot.strat.ghosts and self.bot.townhalls.same_tech({UnitTypeId.COMMANDCENTER}).amount >= 2:
            await self.build(UnitTypeId.GHOSTACADEMY)
        if self.bot.structures(UnitTypeId.ARMORY).amount < 1 and self.bot.structures(UnitTypeId.FACTORY).amount >= 1 and self.bot.can_afford(UnitTypeId.ARMORY) and self.bot.tech_requirement_progress(UnitTypeId.ARMORY) == 1 and (self.bot.strat.thors or self.bot.strat.spam_helions) and self.bot.townhalls.same_tech({UnitTypeId.COMMANDCENTER}).amount >= 2:
            await self.build(UnitTypeId.ARMORY)
        if self.bot.minerals >= 700 and self.bot.structures(UnitTypeId.BARRACKS).amount < 25:
            await self.build(UnitTypeId.BARRACKS)

    async def get_random_build_spot(self, structure, near):
        return await self.bot.find_placement(structure, near, placement_step=2)
    
    def get_build_spot_refinery(self, base):
        for gayser in base.vespene_geysers:
            if self.bot.structures.filter(lambda structure : (structure.type_id == UnitTypeId.REFINERY or 
                                            structure.type_id == UnitTypeId.REFINERYRICH)
                                            and structure.distance_to(gayser.position) < 1).amount == 0:
                return gayser
        return None
    
    async def build(self, structure):
        if structure == UnitTypeId.BARRACKS or structure == UnitTypeId.FACTORY or structure == UnitTypeId.STARPORT:
            await self.build_in_line(structure, BuildingLineWidth.WITHADDONS)
        elif structure == UnitTypeId.ENGINEERINGBAY or structure == UnitTypeId.ARMORY or structure == UnitTypeId.GHOSTACADEMY or structure == UnitTypeId.FUSIONCORE:
            await self.build_in_line(structure, BuildingLineWidth.THREEWIDE)
        elif structure == UnitTypeId.SUPPLYDEPOT:
            await self.build_in_line(structure, BuildingLineWidth.TWOWIDE)
        elif structure == UnitTypeId.COMMANDCENTER:
            await self.build_in_base_location(structure)
        else:
            await self.build_near_base(structure)


    async def build_near_base(self, structure):
        from .base import Base
        group_options = []
        for group in self.bot.root_groups:
            if type(group) == Base:
                if group.base_structure != None and len(group.workers) > 0 and structure != UnitTypeId.REFINERY:
                    where = await self.get_random_build_spot(structure, group.base_structure.get_self().position)
                    group_options.append(Option(self.bot, len(group.workers) * 10, who= group, where= where))
                elif group.base_structure != None and len(group.workers) > 0 and structure == UnitTypeId.REFINERY and len(group.refineries) < len(group.vespene_geysers):
                    where = self.get_build_spot_refinery(group)
                    if where != None:
                        group_options.append(Option(self.bot, len(group.workers) * 10 + where.vespene_contents/10,who= group, where= where))
        if len(group_options) > 0:
            chosen = chose_option(group_options)
            chosen_group = chosen.who
            build_spot = chosen.where
            if build_spot != None and chosen_group != None:
                chosen_group.build(structure, build_spot)
    
    async def build_in_base_location(self, structure = UnitTypeId.COMMANDCENTER):
        location = await self.bot.get_next_expansion()
        base_options = []
        if location != None:
            for base in self.bot.root_groups:
                from .base import Base
                if type(base) == Base and len(base.workers) > 0 and base.center != None:
                    base_option = Option(self.bot, base.center.distance_to(location), base)
                    base_options.append(base_option)
        if len(base_options) > 0:
            nearest_base = chose_lowest_option(base_options).what
            nearest_base.build(structure, location)
            
            

    
    async def build_in_line(self, structure, width = BuildingLineWidth.WITHADDONS, time_out = 5): # TODO: timeout by němělo být pořeba. Zasciklení by nemělo nastávát. Zjisti pročv nastává
        #print(self.bot.root_groups)
        from .base import Base
        from .building_line_group import BuildingLineGroup
        options = []
        for group in self.bot.root_groups:
            if type(group) == BuildingLineGroup and group.width == width:
                where = await group.get_next_structure_position()
                if where:
                    base_options = []
                    for base in self.bot.root_groups:
                        if type(base) == Base and len(base.workers) > 0 and base.center != None:
                            base_option = Option(self.bot, 1000 - base.center.distance_to(where), base)
                            base_options.append(base_option)
                    nearest_base = None
                    if len(base_options) > 0:
                        nearest_base = chose_option(base_options)
                        option = Option(self.bot, nearest_base.motivation, where= where, who= nearest_base.what)
                        options.append(option)
        if len(options) > 0:
            chosen = chose_option(options)
            chosen_group = chosen.who
            build_spot = chosen.where
            if build_spot != None and chosen_group != None:
                chosen_group.build(structure, build_spot)
                return
        await self.get_new_building_line_group(width)
        await self.build_in_line(structure, width, time_out= time_out - 1)
    
    async def get_new_building_line_group(self, width = BuildingLineWidth.WITHADDONS):
        from .base import Base
        from .building_line_group import BuildingLineGroup
        options = []
        for group in self.bot.root_groups:
            if type(group) == Base and group.center != None:
                option = Option(self.bot, len(group.workers) + 1, group)
                options.append(option)
        if len(options) > 0:
            what = chose_option(options).what
            parameters = await self.bot.geometry.get_parameters_for_building_line_group_near(what.center, width= width)
            building_line = BuildingLineGroup(self.bot, [], parameters[0], parameters[1], parameters[2], parameters[3], width= width)
            self.bot.root_groups.append(building_line)
        

    async def build_tree_progresion_structure(self):
        structure = self.get_tree_progression_structure()
        if structure != None and self.bot.can_afford(structure):
            await self.build(structure)

    def get_tree_progression_structure(self):
        structures = self.get_tree_progression_structures()
        if len(structures) > 0:
            structure_options = []
            if UnitTypeId.COMMANDCENTER in structures:
                structure_options.append(Option(self.bot, 100, UnitTypeId.COMMANDCENTER))
            if UnitTypeId.SUPPLYDEPOT in structures:
                structure_options.append(Option(self.bot, 80, UnitTypeId.SUPPLYDEPOT))
            if UnitTypeId.BARRACKS in structures:
                structure_options.append(Option(self.bot, 80, UnitTypeId.BARRACKS))
            if UnitTypeId.FACTORY in structures:
                structure_options.append(Option(self.bot, 50, UnitTypeId.FACTORY))
            if UnitTypeId.STARPORT in structures:
                structure_options.append(Option(self.bot, 30, UnitTypeId.STARPORT))
            if UnitTypeId.ENGINEERINGBAY in structures:
                structure_options.append(Option(self.bot, 30, UnitTypeId.ENGINEERINGBAY))
            if UnitTypeId.REFINERY in structures:
                structure_options.append(Option(self.bot, 70, UnitTypeId.REFINERY))
            if not self.bot.is_upol: 
                if UnitTypeId.ARMORY in structures:
                    structure_options.append(Option(self.bot, 20, UnitTypeId.ARMORY))
                if UnitTypeId.FUSIONCORE in structures:
                    structure_options.append(Option(self.bot, 10, UnitTypeId.FUSIONCORE))
                if UnitTypeId.GHOSTACADEMY in structures:
                    structure_options.append(Option(self.bot, 10, UnitTypeId.GHOSTACADEMY))
            return chose_option(structure_options).what
    
    def get_tree_progression_structures(self):
        tree_progression_structures = []
        structures = self.bot.structures
        if structures.filter(lambda structure : structure.type_id == UnitTypeId.COMMANDCENTER or 
                                            structure.type_id == UnitTypeId.COMMANDCENTERFLYING or 
                                            structure.type_id == UnitTypeId.ORBITALCOMMAND or 
                                            structure.type_id == UnitTypeId.ORBITALCOMMANDFLYING or 
                                            structure.type_id == UnitTypeId.PLANETARYFORTRESS).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.COMMANDCENTER) == 1:
            tree_progression_structures.append(UnitTypeId.COMMANDCENTER)
        if structures.filter(lambda structure : structure.type_id == UnitTypeId.SUPPLYDEPOT or 
                                            structure.type_id == UnitTypeId.SUPPLYDEPOTLOWERED).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.SUPPLYDEPOT) == 1:
            tree_progression_structures.append(UnitTypeId.SUPPLYDEPOT)
        if structures.filter(lambda structure : structure.type_id == UnitTypeId.BARRACKS or 
                                            structure.type_id == UnitTypeId.BARRACKSFLYING).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.BARRACKS) == 1:
            tree_progression_structures.append(UnitTypeId.BARRACKS)
        if structures.filter(lambda structure : structure.type_id == UnitTypeId.FACTORY or 
                                            structure.type_id == UnitTypeId.FACTORYFLYING).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.FACTORY) == 1:
            tree_progression_structures.append(UnitTypeId.FACTORY)
        if structures.filter(lambda structure : structure.type_id == UnitTypeId.STARPORT or 
                                            structure.type_id == UnitTypeId.STARPORTFLYING).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.STARPORT) == 1:
            tree_progression_structures.append(UnitTypeId.STARPORT)
        if structures.filter(lambda structure : structure.type_id == UnitTypeId.REFINERY or 
                                            structure.type_id == UnitTypeId.REFINERYRICH).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.REFINERY) == 1:
            tree_progression_structures.append(UnitTypeId.REFINERY)
        if structures.filter(lambda structure : structure.type_id == UnitTypeId.ENGINEERINGBAY).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.ENGINEERINGBAY) == 1:
                tree_progression_structures.append(UnitTypeId.ENGINEERINGBAY)
        if not self.bot.is_upol:
            if structures.filter(lambda structure : structure.type_id == UnitTypeId.ARMORY).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.ARMORY) == 1:
                tree_progression_structures.append(UnitTypeId.ARMORY)
            if structures.filter(lambda structure : structure.type_id == UnitTypeId.GHOSTACADEMY).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.GHOSTACADEMY) == 1:
                tree_progression_structures.append(UnitTypeId.GHOSTACADEMY)
            if structures.filter(lambda structure : structure.type_id == UnitTypeId.FUSIONCORE).amount == 0 and self.bot.tech_requirement_progress(UnitTypeId.FUSIONCORE) == 1:
                tree_progression_structures.append(UnitTypeId.FUSIONCORE)
        return tree_progression_structures
    
    def add_new_unit_to_lonely_units(self, actual_unit):
        unit = None
        if actual_unit.type_id == UnitTypeId.SCV and self.bot.iteration > 0:
            from .scv import Scv
            unit = Scv(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.MULE:
            from .mule import Mule
            unit = Mule(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.MARINE:
            from .marine import Marine
            unit = Marine(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.MARAUDER:
            from .marauder import Marauder
            unit = Marauder(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.REAPER:
            from .reaper import Reaper
            unit = Reaper(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.GHOST:
            from .ghost import Ghost
            unit = Ghost(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.HELLION or actual_unit.type_id == UnitTypeId.HELLIONTANK:
            from .hellion import Hellion
            unit = Hellion(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.WIDOWMINE:
            from .widow_mine import WidowMine
            unit = WidowMine(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.SIEGETANK:
            from .siege_tank import SiegeTank
            unit = SiegeTank(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.CYCLONE:
            from .cyclone import Cyclone
            unit = Cyclone(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.VIKINGFIGHTER or actual_unit.type_id == UnitTypeId.VIKINGASSAULT:
            from .viking import Viking
            unit = Viking(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.MEDIVAC:
            from .medivac import Medivac
            unit = Medivac(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.LIBERATOR:
            from .liberator import Liberator
            unit = Liberator(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.BANSHEE:
            from .banshee import Banshee
            unit = Banshee(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.RAVEN:
            from .raven import Raven
            unit = Raven(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.BATTLECRUISER:
            from .battlecruiser import Battlecruiser
            unit = Battlecruiser(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        elif actual_unit.type_id == UnitTypeId.THOR:
            from .thor import Thor
            unit = Thor(self.bot, actual_unit.tag)
            self.bot.lonely_units.append(unit)
        return unit
    
    def get_amount_of_structure_pending(self, structure_id):
        counter = 0
        for unit in self.bot.frendly_structures_or_units:
            from .scv import Scv
            if type(unit) == Scv and unit.building_structure == structure_id:
                counter += 1
        return counter

    async def broadcast_new_structure(self, structure):
        for unit in self.bot.lonely_units:
            await unit.on_building_construction_complete(structure)
        for group in self.bot.root_groups:
            await group.on_building_construction_complete(structure)

    async def add_new_structure_to_lonely_units(self, actual_structure):
        if actual_structure.type_id == UnitTypeId.SUPPLYDEPOT:
            from .supply_depot import SupplyDepot
            structure = SupplyDepot(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.COMMANDCENTER and self.bot.iteration > 0:
            from .base_structure import BaseStructure
            structure = BaseStructure(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.BARRACKS:
            from .barrack import Baracks
            structure = Baracks(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.FACTORY:
            from .factory import Factory
            structure = Factory(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.STARPORT:
            from .starport import Starport
            structure = Starport(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.ENGINEERINGBAY:
            from .engeneering_bay import EnergeeringBay
            structure = EnergeeringBay(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.ARMORY:
            from .armory import Armory
            structure = Armory(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.FUSIONCORE:
            from .fusion_core import FusionCore
            structure = FusionCore(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.BUNKER:
            from .bunker import Bunker
            structure = Bunker(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.GHOSTACADEMY:
            from .ghost_academy import GhostAcademy
            structure = GhostAcademy(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure
        elif actual_structure.type_id == UnitTypeId.REFINERY:
            from .refinery import Refinery
            structure = Refinery(self.bot, actual_structure.tag)
            self.bot.lonely_units.append(structure)
            return structure

    def update_is_structure_at_enemy_spawn(self):
        if self.is_structure_at_enemy_spawn:
            for unit in self.bot.frendly_structures_or_units:
                actual_unit = unit.get_self()
                if actual_unit.distance_to(self.bot.enemy_start_locations[0]) < 4:
                    structure = self.bot.geometry.get_nearest_enemy_structure(actual_unit.position, True, False)
                    if structure == None or structure.position.distance_to(actual_unit.position) > 8:
                        self.is_structure_at_enemy_spawn = False