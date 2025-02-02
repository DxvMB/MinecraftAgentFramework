import unittest
from unittest.mock import patch, MagicMock
from MinecraftAgentFramework.framework.agent_manager import AgentManager 


class TestAgentManager2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls.mock_minecraft = MagicMock()
        AgentManager.mc = cls.mock_minecraft

    def setUp(self):
        self.bot_manager = AgentManager()

    @patch("MinecraftAgentFramework.agents.minecraft_agent.Minecraft.create")
    @patch.object(AgentManager, "list_active_bots")
    @patch.object(AgentManager, "stop_bot")
    @patch.object(AgentManager, "start_bot")
    def test_start_all(self, mock_start, mock_stop, mock_list, mock_minecraft):
        
        self.bot_manager.start_all()
        mock_start.assert_any_call("insult_bot")
        mock_start.assert_any_call("oracle_bot")
        mock_start.assert_any_call("tnt_bot")
        self.assertEqual(mock_start.call_count, 4)  

    @patch("MinecraftAgentFramework.framework.agent_manager.AgentManager.read")
    @patch("MinecraftAgentFramework.framework.agent_manager.print")
    def test_read_and_response_start(self, mock_print, mock_read):
        mock_read.side_effect = ["unknown_command", "exit"]  
        self.bot_manager.read_and_response()
        mock_print.assert_any_call("Comando no reconocido. Intente de nuevo.")


    def test_stop_bot(self):
        
        bot_type = "test_bot"
        mock_bot = MagicMock()
        mock_thread = MagicMock()
        self.bot_manager.threads[bot_type] = {"thread": mock_thread, "bot": mock_bot}

        self.bot_manager.stop_bot(bot_type)

        mock_bot.set_run.assert_called_once()  #  set_run()
        mock_thread.join.assert_called_once()  #  join()
        self.assertNotIn(bot_type, self.bot_manager.threads)

    def test_list_active_bots(self):
        # bots simulation
        self.bot_manager.threads = {"bot1": {}, "bot2": {}}
        with patch('builtins.print') as mock_print:  # verify out
            self.bot_manager.list_active_bots()
            mock_print.assert_any_call("Bots activos:")
            mock_print.assert_any_call("- bot1")
            mock_print.assert_any_call("- bot2")


if __name__ == '__main__':
    unittest.main()
