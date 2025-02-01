# agents/TNTBot.py
from MinecraftAgentFramework.agents.base_agent import MinecraftAgent
from MinecraftAgentFramework.mcpi import block
import random
import time

class TNTBot(MinecraftAgent):
    def run(self):
        while self.running:
            x = random.randint(1, 5)
            z = random.randint(1, 5)
            self.build(block.TNT.id, x, 0, z)
            self.build(block.REDSTONE_BLOCK.id, x, 1, z)
            self.build(block.AIR.id, x, 1, z)
            time.sleep(1)
            self.send_message("TNT ignited!")
            time.sleep(3)
