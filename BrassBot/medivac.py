from .unit import Unit
from .option import Option, chose_option, chose_lowest_option

class Medivac(Unit):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
        self.can_autoattack = False
    
    async def on_step(self):
        await super().on_step()
        self.form_and_copy_task_from_parent()

    def do_sieging(self):
        if self.try_healing():
            return
        return super().do_sieging()

    def do_fleeing_and_gunning(self):
        if self.try_healing():
            return
        return super().do_fleeing_and_gunning()

    def do_attacking_carefully(self):
        if self.try_healing():
            return
        return super().do_attacking_carefully()

    def do_attacking(self):
        if self.try_healing():
            return
        return super().do_attacking()
    
    def try_healing(self):
        healable_in_range = []
        if self.get_self():
            healable_in_range = self.bot.units.closer_than(4 + self.get_self().radius, self.get_self().position).filter(lambda unit:  unit.is_biological and unit.health_percentage < 100)
        if len(healable_in_range) > 0:
            options = []
            for unit in healable_in_range:
                option = Option(self.bot, unit.health_percentage, unit)
                options.append(option)
            target = chose_lowest_option(options).what
            self.get_self().attack(target)
            return True
        return False