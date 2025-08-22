from .unit import Unit
from .tasks import Task
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.buff_id import BuffId

class StimableUnit(Unit):
    def do_attacking(self):
        if self.should_stim():
            self.stim()
        else:
            return super().do_attacking()
        
    def do_sieging(self):
        if self.should_stim():
            self.stim()
        else:
            return super().do_sieging()

    def should_stim(self) -> bool:
        if self.bot.already_pending_upgrade(UpgradeId.STIMPACK) == 1 and not (self.get_self().has_buff(BuffId.STIMPACK) or self.get_self().has_buff(BuffId.STIMPACKMARAUDER)) and len(self.get_enemies_in_range(bonus_range = 2, only_revealed=True)) > 0 and self.get_self().shield_health_percentage > 0.5:
            return True
        return False

    def stim(self):
        pass