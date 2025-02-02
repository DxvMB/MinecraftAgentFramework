import threading
import time

from MinecraftAgentFramework.agents.insult_bot import InsultBot
from MinecraftAgentFramework.agents.oracle_bot import OracleBot
from MinecraftAgentFramework.agents.tnt_bot import TNTBot
from MinecraftAgentFramework.agents.chat_bot import ChatBotAgent
from MinecraftAgentFramework.mcpi.minecraft import Minecraft



class BotManager:
    def __init__(self):
        self.threads = {}
        self.mc = Minecraft.create()

    def start_all(self):
        """
        Inicia todos los bots disponibles (insult_bot, oracle_bot, tnt_bot).
        Si ya están en ejecución, los omite.
        """
        bot_types = ["insult_bot", "oracle_bot", "tnt_bot", "chat_bot"]

        for bot_type in bot_types:
            self.start_bot(bot_type)

    def start_bot(self, bot_type):
        if bot_type == "insult_bot":
            bot = InsultBot("Insult Bot")
        elif bot_type == "oracle_bot":
            bot = OracleBot("Oracle Bot")
        elif bot_type == "tnt_bot":
            bot = TNTBot("TNT Bot")
        elif bot_type == "chat_bot":
            bot = ChatBotAgent("facebook/opt-350m")
        else:
            print(f"Tipo de bot desconocido: {bot_type}")
            return

        # Si el bot ya está corriendo, no lo iniciamos de nuevo.
        if bot_type in self.threads:
            print(f"{bot_type} ya está en ejecución.")
            return

        # Crear y empezar el thread
        bot_thread = threading.Thread(target=bot.run, daemon=True)
        self.threads[bot_type] = {"thread": bot_thread, "bot": bot}
        bot_thread.start()
        print(f"{bot_type} ha sido iniciado.")

    def stop_bot(self, bot_type):
        if bot_type in self.threads:
            print(f"Deteniendo {bot_type}...")
            bot_data = self.threads[bot_type]  # Obtener los datos del bot.
            bot_instance = bot_data["bot"]  # Obtenemos el bot asociado.
            bot_instance.set_run()  # Llamar a set_run(False) al bot.
            bot_data["thread"].join()  # Esperar a que termine el hilo.
            del self.threads[bot_type]  # Eliminar de la lista de hilos activos.
            print(f"{bot_type} detenido con éxito.")
        else:
            print(f"{bot_type} no está en ejecución.")


    def list_active_bots(self):
        print("Bots activos:")
        for bot_type in self.threads.keys():
            print(f"- {bot_type}")

    def read(self):
        chat_posts = self.mc.events.pollChatPosts()
        if chat_posts:  # Si existen mensajes en el chat
            message = chat_posts[0].message  # Recuperar el mensaje del primer evento
            return message
        else:
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
