# agents/base_agent.py
from ..mcpi.minecraft import Minecraft
from ..mcpi import block

mc = Minecraft.create()


class MinecraftAgent:
    def __init__(self, name):
        self.name = name
        self.position = mc.player.getTilePos()

    def move(self, x, y, z):
        self.position.x += x
        self.position.y += y
        self.position.z += z
        mc.player.setTilePos(self.position.x, self.position.y, self.position.z)

    def build(self, block_type, dx=0, dy=0, dz=0):
        mc.setBlock(self.position.x + dx, self.position.y + dy, self.position.z + dz, block_type)

    def destroy(self, dx=0, dy=0, dz=0):
        mc.setBlock(self.position.x + dx, self.position.y + dy, self.position.z + dz, block.AIR)

    def send_message(self, message):
        mc.postToChat(f"{self.name}: {message}")

    def invoke_method(self, method_name, *args, **kwargs):
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if callable(method):
                return method(*args, **kwargs)
        raise AttributeError(f"{self.name} has no method '{method_name}'")