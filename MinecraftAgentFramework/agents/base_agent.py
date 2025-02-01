# agents/BaseAgent.py
from ..mcpi.minecraft import Minecraft
import threading

mc = Minecraft.create()
mc_lock = threading.Lock()



class MinecraftAgent:
    def __init__(self, name):
        self.name = name
        self.running = True
        with mc_lock:
            self.position = mc.player.getTilePos()

    def move(self, x, y, z):
        self.position.x += x
        self.position.y += y
        self.position.z += z
        mc.player.setTilePos(self.position.x, self.position.y, self.position.z)

    def build(self, block_type, dx, dy, dz):
        mc.setBlock(self.get_current_position().x + dx, self.get_current_position().y + dy, self.get_current_position().z + dz, block_type)

    def send_message(self, message):
        mc.postToChat(f"{self.name}: {message}")

    def invoke_method(self, method_name, *args, **kwargs):
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if callable(method):
                return method(*args, **kwargs)
        raise AttributeError(f"{self.name} has no method '{method_name}'")

    @staticmethod
    def read_and_respond():
        with mc_lock:
            chat_posts = mc.events.pollChatPosts()

        if chat_posts:  # Si existen mensajes en el chat
            message = chat_posts[0].message  # Recuperar el mensaje del primer evento
            return message
        else:
            return None

    @staticmethod
    def get_current_position():
        with mc_lock:
            return mc.player.getTilePos()

    def set_run(self):
        self.running = False
