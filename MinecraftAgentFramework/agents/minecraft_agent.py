from MinecraftAgentFramework.mcpi.minecraft import Minecraft
import threading

mc_lock = threading.Lock()

class MinecraftAgent:
    mc = None

    @classmethod
    def initialize_minecraft(cls):
        if cls.mc is None:
            cls.mc = Minecraft.create()

    def __init__(self, name):
        MinecraftAgent.initialize_minecraft()
        self.name = name
        self.running = True
        with mc_lock:
            self.position = MinecraftAgent.mc.player.getTilePos()

    def move(self, x, y, z):
        new_position = self._calculate_new_position(x, y, z)
        self._update_position(new_position)
        self._set_player_position(new_position)

    def _calculate_new_position(self, x, y, z):
        return Position(
            self.position.x + x,
            self.position.y + y,
            self.position.z + z
        )

    def _update_position(self, new_position):
        self.position = new_position

    def _set_player_position(self, position):
        MinecraftAgent.mc.player.setTilePos(position.x, position.y, position.z)

    def build(self, block_type, dx, dy, dz):
        position = self._calculate_build_position(dx, dy, dz)
        self._place_block(position, block_type)

    def _calculate_build_position(self, dx, dy, dz):
        current_position = self.get_current_position()
        return Position(
            current_position.x + dx,
            current_position.y + dy,
            current_position.z + dz
        )

    def _place_block(self, position, block_type):
        MinecraftAgent.mc.setBlock(position.x, position.y, position.z, block_type)

    def send_message(self, message):
        MinecraftAgent.mc.postToChat(f"{self.name}: {message}")

    def invoke_method(self, method_name, *args, **kwargs):
        method = self._get_method(method_name)
        return self._execute_method(method, *args, **kwargs)

    def _get_method(self, method_name):
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if callable(method):
                return method
        raise AttributeError(f"{self.name} has no method '{method_name}'")

    def _execute_method(self, method, *args, **kwargs):
        return method(*args, **kwargs)

    @staticmethod
    def read_and_respond():
        with mc_lock:
            chat_posts = MinecraftAgent.mc.events.pollChatPosts()

        return MinecraftAgent._extract_message(chat_posts)

    @staticmethod
    def _extract_message(chat_posts):
        if chat_posts:
            return chat_posts[0].message
        return None

    @staticmethod
    def get_current_position():
        with mc_lock:
            return Position(*MinecraftAgent.mc.player.getTilePos())

    def set_run(self):
        self.running = False

class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
