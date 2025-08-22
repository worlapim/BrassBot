from .unit import Unit
from .tasks import Task
from sc2.ids.ability_id import AbilityId

class Reaper(Unit):
    
    async def on_step(self):
        if self.parent == None:
            success = self.join_closest_sieging_group()
            if not success and self.get_self().health >= 60:
                self.task = Task.ATTACKING
        else:
            self.form_and_copy_task_from_parent()
        await super().on_step()

    def try_kd8_charge(self): 
        actual_self = self.get_self()
        actual_nearest_enemy = self.get_nearest_enemy(can_air=False) # TODO: nejbližší nutně není nejvhodnější, doplnit lepší volbu
        if actual_nearest_enemy != None and actual_nearest_enemy.position.distance_to(actual_self.position) <= 5 and AbilityId.KD8CHARGE_KD8CHARGE in self.abilities:
            actual_self(AbilityId.KD8CHARGE_KD8CHARGE, actual_nearest_enemy.position)
            return True # TODO po tom, co je tohle zavoláno, možná queue další akci
        return False
    
    def do_sieging(self):
        if self.try_kd8_charge():
            return
        return super().do_sieging()

    def do_fleeing_and_gunning(self):
        if self.try_kd8_charge():
            return
        return super().do_fleeing_and_gunning()

    def do_attacking_carefully(self):
        if self.try_kd8_charge():
            return
        return super().do_attacking_carefully()

    def do_attacking(self):
        if self.try_kd8_charge():
            return
        if self.get_self().health < 25 and len(self.get_threats(2)) > 0:
            self.do_fleeing_and_gunning()
            self.task = Task.FLEEING_AND_GUNNING
        elif self.parent != None:
            super().attack()
        else:
            self.lonely_attack()