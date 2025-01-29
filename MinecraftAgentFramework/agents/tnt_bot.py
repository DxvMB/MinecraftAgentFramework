# agents/tnt_bot.py
from ..agents.base_agent import MinecraftAgent
from ..mcpi import block
import random
import time

class TNTBot(MinecraftAgent):
    def run(self):
        while True:
            self.build(block.TNT.id, dx=random.randint(1, 5), dy=0, dz=random.randint(1, 5))
            time.sleep(1)
            self.send_message("TNT ignited!")
            time.sleep(3)