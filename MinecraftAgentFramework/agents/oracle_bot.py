# agents/oracle_bot.py
from ..agents.base_agent import MinecraftAgent
import random
import time

class OracleBot(MinecraftAgent):
    def run(self):
        answers = ["Yes.", "No.", "Maybe.", "42.", "Ask again later."]
        while True:
            self.send_message(f"Answer: {random.choice(answers)}")
            time.sleep(random.randint(2, 5))