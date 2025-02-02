# agents/BaseAgent.py
from MinecraftAgentFramework.mcpi.minecraft import Minecraft
import threading

mc_lock = threading.Lock()



class MinecraftAgent:
    def __init__(self, name):
        self.name = name
        self.running = True
        self.mc = Minecraft.create()
        with mc_lock:
            self.position = self.mc.player.getTilePos()

    def move(self, x, y, z):
        self.position.x += x
        self.position.y += y
        self.position.z += z
        self.mc.player.setTilePos(self.position.x, self.position.y, self.position.z)

    def build(self, block_type, dx, dy, dz):
        self.mc.setBlock(self.get_current_position().x + dx, self.get_current_position().y + dy, self.get_current_position().z + dz, block_type)

    def send_message(self, message):
        self.mc.postToChat(f"{self.name}: {message}")

    def invoke_method(self, method_name, *args, **kwargs):
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if callable(method):
                return method(*args, **kwargs)
        raise AttributeError(f"{self.name} has no method '{method_name}'")

    def read_and_respond(self):
        with mc_lock:
            chat_posts = self.mc.events.pollChatPosts()

        if chat_posts:  # Si existen mensajes en el chat
            message = chat_posts[0].message  # Recuperar el mensaje del primer evento
            return message
        else:
            return None

    def get_current_position(self):
        with mc_lock:
            return self.mc.player.getTilePos()

    def set_run(self):
        self.running = False
