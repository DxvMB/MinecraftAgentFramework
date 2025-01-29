from agents.insult_bot import InsultBot
from agents.tnt_bot import TNTBot
from agents.oracle_bot import OracleBot
from framework.agent_framework import AgentFramework
import time

if __name__ == "__main__":
    framework = AgentFramework()
    framework.register_agent(InsultBot("InsultBot"))
    framework.register_agent(TNTBot("TNTBot"))
    framework.register_agent(OracleBot("OracleBot"))
    threads = framework.start_all()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation ended.")