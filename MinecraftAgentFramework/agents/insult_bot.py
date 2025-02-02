import minecraft_agent
import random
import time

class InsultBot(MinecraftAgent):
    def run(self):
        insults = ["You build like a zombie!", "Is that dirt you're working with?", "My code is smarter than you!"]
        while self.running:
            self.send_message(random.choice(insults))
            time.sleep(random.randint(2, 5))
        return None
