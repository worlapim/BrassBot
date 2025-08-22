from .group import Group
from .tasks import Task

class ArmyGroup(Group):
    
    async def on_before_step(self):
        await super().on_before_step()
        if self.bot.time % 125 < 5 and self.bot.time >= 300 and self.task == Task.NOTHING:
            self.task = Task.SIEGING
        if self.task == Task.SIEGING and len(list(filter(lambda x: x.task != Task.JOINING, self.members))) < 6:
            self.task = Task.NOTHING
        if self.center:
            nearest_enemy = self.get_nearest_enemy()
            if nearest_enemy != None and self.weighted_center != None and nearest_enemy.distance_to(self.weighted_center) < 35:
                self.attacking_target = nearest_enemy
            else:
                self.attacking_target = None
            if self.attacking_target and self.task != Task.SIEGING:
                self.task = Task.ATTACKING
            elif self.task == Task.SIEGING:
                self.destination = self.attacking_target 
                if self.destination == None:
                    self.destination = self.get_nearest_enemy_structure()
                if self.destination == None:
                    self.destination = self.bot.enemy_start_locations[0]
                if self.weighted_center.distance_to(self.destination) < 5:
                    self.task = Task.SCOUTING
                    self.get_random_hidden_destination()
            elif self.task == Task.SCOUTING:
                if self.destination == None:
                    self.destination = self.bot.geometry.get_random_spot()
                nearest_enemy = self.get_nearest_enemy_structure()
                if nearest_enemy != None:
                    self.task = Task.SIEGING
                    self.destination = nearest_enemy.position
                if self.weighted_center.distance_to(self.destination) < 5:
                    self.get_random_hidden_destination()
            else:
                self.task = Task.NOTHING
        

    async def on_after_step(self):
        await super().on_after_step()
    
    async def on_step(self):
        # filtered = list(filter(lambda member: not member.is_active, self.members))
        # self.bot.chat.add_to_chat_queue(len(filtered))
        # for unit in filtered:
        #     self.bot.chat.add_to_chat_queue(unit.is_active)
        # print(self.center, "center")
        # print(self.weighted_center, "weighted_center")
        await super().on_step()