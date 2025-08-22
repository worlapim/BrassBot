from .unit import Unit
from sc2.ids.ability_id import AbilityId

class Raven(Unit):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
        self.can_autoattack = False
    
    async def on_step(self):
        await super().on_step()
        self.form_and_copy_task_from_parent()

    def try_antiarmor_missile(self): 
        actual_self = self.get_self()
        actual_nearest_enemy = self.get_nearest_enemy(can_air=False) # TODO: nejbližší nutně není nejvhodnější, doplnit lepší volbu; kontrolovat, jestli jsou okolo v;bec spojenci, co toho efektu využijou
        if actual_nearest_enemy != None and actual_nearest_enemy.position.distance_to(actual_self.position) <= 10 and self.get_self().energy >= 75:
            actual_self(AbilityId.EFFECT_ANTIARMORMISSILE, actual_nearest_enemy)
            return True # TODO po tom, co je tohle zavoláno, možná queue další akci
        return False
    
    #AbilityId.BUILDAUTOTURRET_AUTOTURRET
    
    def siege(self):
        if self.try_antiarmor_missile():
            return
        return super().siege()
        
    def attack(self):
        if self.try_antiarmor_missile():
            return
        return super().attack()