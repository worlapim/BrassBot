class EnemyInfo():
    def __init__(self,bot):
        self.bot = bot
        self.is_doing_air = False
    
    
    async def on_step(self):
        if self.bot.enemy_units.flying().exclude_type(set(self.bot.static_instructions.nonthreatening_air_units)).amount > self.bot.time / 300:
            self.is_doing_air = True
