import threading
from http.client import responses

from MinecraftAgentFramework.agents.InsultBot import InsultBot
from MinecraftAgentFramework.agents.TNTBot import TNTBot
from MinecraftAgentFramework.agents.OracleBot import OracleBot
from MinecraftAgentFramework.framework.AgentManager import BotManager
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

