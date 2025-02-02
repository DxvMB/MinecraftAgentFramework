# agents/OracleBot.py
import time

from MinecraftAgentFramework.agents.base_agent import MinecraftAgent
from MinecraftAgentFramework.mcpi import block


class OracleBot(MinecraftAgent):
    def run(self):
        while self.running:
            chat_message = self.read_and_respond()
            if str(chat_message).lower() == "hola":
                self.send_message("Hola! En que puedo ayudarte en el mundo de Minecraft?")
                time.sleep(3)
            elif str(chat_message).lower() == "posicion":
                pos = self.get_current_position()
                self.send_message(f"Actualmente estoy en las coordenadas: x={pos.x}, y={pos.y}, z={pos.z}.")
                time.sleep(3)
            elif str(chat_message).lower() == "construye":
                self.build(block.WOOD.id, 1, 0, 0)  # Construye un bloque de madera a un lado.
                self.send_message("Me he construido un bloque de madera")
                time.sleep(3)
            elif str(chat_message).lower() == "mueve":
                self.move(1, 0, 0)  # Mueve al agente 1 bloque hacia adelante.
                self.send_message("Me he movido un bloque hacia adelante")
                time.sleep(3)
