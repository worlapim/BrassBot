import random

class Strat():
    def __init__(self,bot):
        self.bot = bot
        self.spam_helions = False
        self.tech_tree = False
        self.ghosts = False
        self.reapers = False
        self.thors = False
    
    async def on_step(self):
        if self.bot.enemy_info.is_doing_air:
            self.thors = True
            self.spam_helions = False
            self.reapers = False


    def chose_strat_for_start(self, is_upol):
        if is_upol or random.randint(1,2) == 2:
            self.spam_helions = True
            self.reapers = True
        else:
            self.ghosts = True