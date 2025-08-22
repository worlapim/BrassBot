from .tasks import Task
import time

class Group():

    def __init__(self, bot, members = []):
        self.bot = bot
        self.members = members
        self.task = Task.NOTHING
        self.parent = None
        self.center = self.get_center()
        self.weighted_center = self.get_weighted_center()
        self.attacking_target = None
        self.destination = None
        self.can_air = False
        self.can_ground = False
        for member in self.members:
            member.parent = self

    async def on_before_step(self):
        self.center = self.get_center()
        self.weighted_center = self.get_weighted_center()
        self.update_can_air_and_ground()
        self.check_that_not_all_joining()
        for member in self.members:
            if member in self.bot.lonely_units:
                self.bot.lonely_units.remove(member)
                member.parent = self
            await member.on_before_step()

    async def on_after_step(self):
        for member in self.members:
            await member.on_after_step()
    
    async def on_step(self):
        for member in self.members:
            await member.on_step()
                
    async def on_unit_destroyed(self,victim):
        for member in self.members:
            if await member.on_unit_destroyed(victim):
                self.members.remove(member)
                return True
            
    async def on_building_construction_complete(self, unit):
        for member in self.members:
            await member.on_building_construction_complete(unit)

    def get_center(self):
        active_members = list(filter(lambda member: member.is_active, self.members))
        if len(active_members) > 0:
            return self.bot.geometry.get_center_of_abstract_units(active_members)
        return None
    
    def update_can_air_and_ground(self):
        self.can_air = False
        self.can_ground = False
        for member in self.members:
            actual_member = member.get_self()
            if actual_member != None and member.task != Task.JOINING:
                if actual_member.can_attack_air or actual_member.can_attack_both:
                    self.can_air = True
                if actual_member.can_attack_ground or actual_member.can_attack_both:
                    self.can_ground = True
    
    def check_that_not_all_joining(self):
        if len(self.members) > 0:
            not_joining_members = list(filter(lambda member: member.task != Task.JOINING and member.is_active, self.members))
            if len(not_joining_members) == 0:
                for member in self.members:
                    member.task = Task.NOTHING
        
    def get_weighted_center(self):
        not_joining_members = list(filter(lambda member: member.task != Task.JOINING and member.is_active, self.members))
        if len(not_joining_members) > 0:
            weigted_center = self.bot.geometry.get_center_of_abstract_units(not_joining_members)
            if weigted_center.x == 0 and weigted_center.y == 0:
                weigted_center = None
            return weigted_center
        return None
        
    def get_nearest_enemy(self, can_ground = None, can_air = None, only_revealed = False):
        if can_ground == None:
            can_ground = self.can_ground
        if can_air == None:
            can_air = self.can_air
        if self.weighted_center != None:
            enemy = self.bot.geometry.get_nearest_enemy(self.weighted_center, can_ground, can_air, only_revealed)
            return enemy
        enemy = self.bot.geometry.get_nearest_enemy(self.center, can_ground, can_air, only_revealed)
        return enemy
    
    def get_mele_the_threads(self, radius):
        if self.weighted_center != None:
            return self.bot.enemy_units.filter(lambda unit : unit.ground_range < 2 and not unit._proto.is_flying).closer_than(radius, self.weighted_center)
        elif self.center != None:
            return self.bot.enemy_units.filter(lambda unit : unit.ground_range < 2 and not unit._proto.is_flying).closer_than(radius, self.center)
        return []
    
    def get_nearest_enemy_structure(self, can_ground = None, can_air = None):
        if can_ground == None:
            can_ground = self.can_ground
        if can_air == None:
            can_air = self.can_air
        if self.weighted_center != None:
            enemy = self.bot.geometry.get_nearest_enemy_structure(self.weighted_center, can_ground, can_air)
            return enemy
        enemy = self.bot.geometry.get_nearest_enemy_structure(self.center, can_ground, can_air)
        return enemy
    
    
    def get_random_hidden_destination(self):
        self.destination = self.bot.geometry.get_random_hidden_destination()