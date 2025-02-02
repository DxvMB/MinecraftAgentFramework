import threading
import time

import importlib

from MinecraftAgentFramework.agents.minecraft_agent import MinecraftAgent
from MinecraftAgentFramework.agents.insult_bot import InsultBot
from MinecraftAgentFramework.agents.oracle_bot import OracleBot
from MinecraftAgentFramework.agents.tnt_bot import TNTBot
from MinecraftAgentFramework.agents.chat_bot import ChatBot
from MinecraftAgentFramework.mcpi.minecraft import Minecraft


class AgentManager:
    mc = None

    @classmethod
    def initialize_minecraft(cls):
        if cls.mc is None:
            cls.mc = Minecraft.create()

    def __init__(self):
        AgentManager.initialize_minecraft()
        self.threads = {}

    def start_all(self):
        """
        Inicia todos los bots disponibles (insult_bot, oracle_bot, tnt_bot, chat_bot).
        Si ya están en ejecución, los omite.
        """
        bot_types = ["insult_bot", "oracle_bot", "tnt_bot", "chat_bot"]
        for bot_type in bot_types:
            self.start_bot(bot_type)

    def start_bot(self, bot_type):
        if bot_type in self.threads:
            print(f"{bot_type} ya está en ejecución.")
            return

        bot = self._create_bot(bot_type)
        if bot is None:
            return

        bot_thread = threading.Thread(target=bot.run, name=bot_type , daemon=True)
        self.threads[bot_type] = {"thread": bot_thread, "bot": bot}
        bot_thread.start()
        print(f"{bot_type} ha sido iniciado.")

    def _create_bot(self, bot_type):
        try:
            # Mapeo de bot_type a la clase correspondiente
            bot_type_to_class = {
                "insult_bot": "InsultBot",
                "oracle_bot": "OracleBot",
                "tnt_bot": "TNTBot",
                "chat_bot": "ChatBot"  # Asegúrate de que el nombre de la clase sea correcto
            }

            # Verificamos que bot_type esté en el diccionario
            if bot_type not in bot_type_to_class:
                print(f"Tipo de bot desconocido: {bot_type}")
                return None

            # Obtenemos el nombre de la clase del diccionario
            bot_class_name = bot_type_to_class[bot_type]

            # Importamos el módulo correspondiente
            module = importlib.import_module(f"MinecraftAgentFramework.agents.{bot_type}")
            bot_class = getattr(module, bot_class_name)

            # Inicializamos el bot con el nombre correcto del modelo
            if bot_type == "chat_bot":
                # Usamos un modelo válido de Hugging Face, por ejemplo, "facebook/opt-350m"
                return bot_class("facebook/opt-350m")
            else:
                # Proporcionamos un nombre durante inicialización para otros bots
                return bot_class(bot_class_name.replace('Bot', ''))
        except (ImportError, AttributeError) as e:
            print(f"Error al crear bot {bot_type}: {e}")
            return None

    def stop_bot(self, bot_type):
        if bot_type not in self.threads:
            print(f"{bot_type} no está en ejecución.")
            return

        print(f"Deteniendo {bot_type}...")
        bot_data = self.threads[bot_type]
        bot_instance = bot_data["bot"]
        bot_instance.set_run()
        bot_data["thread"].join()
        del self.threads[bot_type]
        print(f"{bot_type} detenido con éxito.")

    def list_active_bots(self):
        print("Bots activos:")
        for bot_type in self.threads.keys():
            print(f"- {bot_type}")

    @staticmethod
    def read():
        chat_posts = AgentManager.mc.events.pollChatPosts()
        return AgentManager._extract_message(chat_posts)

    @staticmethod
    def _extract_message(chat_posts):
        if chat_posts:
            return chat_posts[0].message
        return None

    def read_and_response(self):
        while True:
            command = self.read()
            if command is None:
                time.sleep(1)
            else:
                if  command.startswith("start"):
                    bot_type = command.split(" ", 1)[1]
                    self.start_bot(bot_type)
                elif command.startswith("stop"):
                    bot_type = command.split(" ", 1)[1]
                    self.stop_bot(bot_type)
                elif command == "list":
                    self.list_active_bots()
                elif command == "exit":
                    print("Saliendo del programa...")
                    break
                else:
                    print("Comando no reconocido. Intente de nuevo.")
