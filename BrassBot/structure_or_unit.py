from .tasks import Task
from .option import Option, chose_option, chose_lowest_option
from sc2.ids.unit_typeid import UnitTypeId
import time
from sc2.unit import Unit as ActualUnit
from typing import Optional

class StructureOrUnit():
    def __init__(self, bot, tag):
        self.bot = bot
        self.tag = tag
        self.task = Task.NOTHING
        self.parent = None
        self.position = None
        self.type_id = None
        self.actual_unit = None
        self.time_not_updated_actual_unit = 9000
        self.destination = None
        self.is_destination_reachable = True
        self.abilities = []
        self.can_autoattack = True
        self.previous_flee_direction = None
        self.is_active = True
        self.update_self()

    def get_self(self) -> Optional[ActualUnit]:
        return self.actual_unit
        
    
    def update_self(self):
        actual_unit = (self.bot.structures + self.bot.units).filter(lambda unit : unit.tag == self.tag)
        if len(actual_unit) > 0:
            self.actual_unit = actual_unit[0]
            self.time_not_updated_actual_unit = 0
        else:
            self.time_not_updated_actual_unit += 1
        self.is_active = not self.get_self().is_memory
    
    async def on_step(self):
        actual_unit = self.get_self()
        if actual_unit:
            if self.task == Task.NOTHING:
                self.do_nothing()
            elif self.task == Task.OTHER:
                self.do_other()
            elif self.task == Task.MINING:
                self.do_mining()
            elif self.task == Task.GASS_MINING:
                self.do_gass_mining()
            elif self.task == Task.BUILDING:
                self.do_building()
            elif self.task == Task.FLEEING:
                self.do_fleeing()
            elif self.task == Task.FLEEING_AND_GUNNING:
                self.do_fleeing_and_gunning()
            elif self.task == Task.ATTACKING:
                self.do_attacking()
            elif self.task == Task.ATTACKING_CAREFULLY:
                self.do_attacking_carefully()
            elif self.task == Task.SCOUTING:
                self.do_scouting()
            elif self.task == Task.SIEGING:
                self.do_sieging()
            elif self.task == Task.JOINING:
                self.do_joining()
            elif self.task == Task.DEFENDING:
                self.do_defending()

    async def on_before_step(self):
        self.update_self()
        if self.get_self().type_id in [UnitTypeId.REAPER, UnitTypeId.GHOST, UnitTypeId.GHOSTACADEMY, UnitTypeId.THOR]:
            self.abilities = await self.bot.get_available_abilities(self.get_self())
        if self.destination != None:
            distance = await self.bot._client.query_pathing(self.get_self().position, self.destination)
            self.is_destination_reachable = distance != None
        else:
            self.is_destination_reachable = True

    async def on_after_step(self):
        pass

    async def on_unit_destroyed(self,victim):
        if self.tag == victim:
            # await self.bot.chat.say(str(self)+ " zničen")
            return True
        
    async def on_building_construction_complete(self, unit):
        pass

    def flee(self):
        actual_unit = self.get_self()
        if actual_unit:
            self.previous_flee_direction = actual_unit.position.towards((actual_unit.position + self.bot.geometry.get_best_exit_route(actual_unit.position, self.previous_flee_direction, not actual_unit.is_flying)), actual_unit.calculate_speed())
            actual_unit.move(self.previous_flee_direction)

    def siege(self):
        pass

    def get_threats(self, extra_range = 0, exclude_workers = False):
        actual_unit = self.get_self()
        if actual_unit:
            return self.bot.geometry.get_threats(actual_unit.position, not actual_unit.is_flying, extra_range, exclude_workers)
        else:
            return []
        
    def get_nearby_enemy_structures(self, range = None, structure_filter = None, only_ready = False):
        if range == None:
            range = self.get_self().ground_range
        if range == None or range == 0:
            range = 8
        return self.bot.geometry.get_nearby_enemy_structures(self.get_self().position, range, structure_filter, only_ready)
        
    def nearest_army_group(self):
        from .army_group import ArmyGroup
        armmy_groups = []
        for group in self.bot.root_groups:
            if type(group) == ArmyGroup:
                actual_unit = self.get_self()
                if group.center:
                    armmy_groups.append(Option(self.bot,1000 - actual_unit.position.distance_to(group.center) ,what = group))
                else:
                    armmy_groups.append(Option(self.bot, 1, what = group))
        if len(armmy_groups) == 0:
            return None
        return chose_option(armmy_groups).what
    
    def get_nearest_enemy(self, can_ground = True, can_air = True, only_revealed = False):
        enemy = self.bot.geometry.get_nearest_enemy(self.get_self().position, can_ground, can_air, only_revealed)
        return enemy
    
    def get_enemies_in_range(self, can_ground = True, can_air = True, can_structure = False, bonus_range = 0, only_revealed = False):
        enemies = self.bot.geometry.get_enemies_in_range(self, can_ground, can_air, can_structure, bonus_range, only_revealed)
        return enemies
    
    def get_enemy_detectors_in_range(self, can_ground = True, can_air = True, can_structure = False, bonus_range = 0, only_revealed = False):
        enemies = self.get_enemies_in_range(can_ground, can_air, can_structure, bonus_range, only_revealed)
        detectors = list(filter(lambda enemy: enemy.type_id in self.bot.static_instructions.detectors, enemies))
        return detectors
    
    def get_threatening_area_effects(self):
        threatening_area_effects = self.bot.geometry.get_threatening_area_effects_for_position(self.get_self().position,self.get_self().radius)
        return threatening_area_effects

    def join_closest_sieging_group(self):
        from .army_group import ArmyGroup
        sieging_groups = list(filter(lambda group: group.task == Task.SIEGING and isinstance(group, ArmyGroup), self.bot.root_groups))
        if len(sieging_groups) > 0:
            options = []
            for group in sieging_groups:
                motivation = 9000
                if group.weighted_center != None:
                   motivation = group.weighted_center.distance_to(self.get_self()) 
                elif group.center != None:
                   motivation = group.center.distance_to(self.get_self())
                option = Option(self.bot, motivation, what= group)
                options.append(option)
            chosen = chose_lowest_option(options)
            if chosen != None:
                self.join(option.what)
                return True
        return False

    def join(self, group):
        group.members.append(self)
        self.parent = group
        self.task = Task.JOINING
        if self in self.bot.lonely_units:
            self.bot.lonely_units.remove(self)

    def leave(self):
        group = self.parent
        if group:
            group.members.remove(self)
        self.parent = None
        self.task = Task.NOTHING
        self.bot.lonely_units.append(self)
    
    def do_nothing(self):
        pass

    def do_other(self):
        pass

    def do_mining(self):
        pass

    def do_gass_mining(self):
        pass

    def do_building(self):
        pass

    def do_fleeing(self):
        pass

    def do_fleeing_and_gunning(self):
        pass

    def do_attacking(self):
        pass

    def do_attacking_carefully(self):
        pass

    def do_scouting(self):
        pass

    def do_sieging(self):
        pass

    def do_joining(self):
        pass

    def do_defending(self):
        pass

    def __str__(self):
        return str(self.__class__.__name__)