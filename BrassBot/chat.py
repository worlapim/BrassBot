import random

class Chat():
    greetings = ["I am new here, please be gentle.","Hello there.", "GL HF", "Let's see, how this game goes."]

    def __init__(self,bot):
        self.bot = bot
        self.chat_queue = []
    
    async def say(self, message):
        await self.bot.chat_send(str(message))

    async def hello(self):
        await self.say(self.greetings[random.randint(0,len(self.greetings) - 1)])

    def add_to_chat_queue(self, message):
        self.chat_queue.append(message)
    
    async def say_chat_queue(self):
        messages = ""
        for message in self.chat_queue:
            messages += str(message) + " "
        await self.say(messages)
        self.chat_queue = []
        