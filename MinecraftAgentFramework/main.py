import threading
from http.client import responses

from MinecraftAgentFramework.agents.insult_bot import InsultBot
from MinecraftAgentFramework.agents.tnt_bot import TNTBot
from MinecraftAgentFramework.agents.oracle_bot import OracleBot
from MinecraftAgentFramework.framework.agent_manager import BotManager
import time



if __name__ == "__main__":
    agent_framework = BotManager()
    agent_framework.start_all()
    response_thread = threading.Thread(target=agent_framework.read_and_response, daemon=True)
    response_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation ended.")

