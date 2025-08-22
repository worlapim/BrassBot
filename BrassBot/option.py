import random

class Option():
    def __init__(self, bot, motivation, what = None, who = None, where = None):
        self.bot = bot
        self.motivation = motivation
        self.what = what
        self.who = who
        self.where = where

def chose_option(options) -> Option:
    if len(options) > 0:
        max_motivation = options[0].motivation
        max_options = []
        for option in options:
            if option.motivation > max_motivation:
                max_motivation = option.motivation
                max_options = [option]
            elif option.motivation == max_motivation:
                max_options.append(option)
        return max_options[random.randint(0,len(max_options) - 1)]
    
def chose_lowest_option(options) -> Option:
    if len(options) > 0:
        min_motivation = options[0].motivation
        min_options = []
        for option in options:
            if option.motivation < min_motivation:
                min_motivation = option.motivation
                min_options = [option]
            elif option.motivation == min_motivation:
                min_options.append(option)
        return min_options[random.randint(0,len(min_options) - 1)]

def chose_probability_option(options):
    if len(options) > 0:
        all_motivation = 0
        for option in options:
            all_motivation += option.motivation
        chosen_motivation = random.randint(0, all_motivation)
        i = -1
        while chosen_motivation > 0:
            i += 1
            chosen_motivation -= options[i].motivation
        return options[i]

