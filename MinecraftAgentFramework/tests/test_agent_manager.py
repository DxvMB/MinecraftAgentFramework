import unittest
import sys
sys.path.append("..")
from unittest.mock import MagicMock, patch
from MinecraftAgentFramework.framework.agent_manager import BotManager


class TestAgentManager(unittest.TestCase):
    @patch("MinecraftAgentFramework.framework.agent_manager.Minecraft.create")  # Mock Minecraft connection
    def setUp(self, mock_minecraft):
        self.mock_minecraft = mock_minecraft.return_value
        self.bot_manager = BotManager()

    @patch("MinecraftAgentFramework.framework.agent_manager.InsultBot")
    @patch("MinecraftAgentFramework.framework.agent_manager.OracleBot")
    @patch("MinecraftAgentFramework.framework.agent_manager.TNTBot")
    @patch("threading.Thread")
    def test_start_bot(self, mock_thread, mock_tnt_bot, mock_oracle_bot, mock_insult_bot):
        # Test starting specific bots
        self.bot_manager.start_bot("insult_bot")
        mock_insult_bot.assert_called_once_with("Insult Bot")
        self.assertIn("insult_bot", self.bot_manager.threads)
        mock_thread.assert_called_once()

        # Test attempting to start the same bot again
        self.bot_manager.start_bot("insult_bot")
        self.assertEqual(mock_thread.call_count, 1)  # No additional thread should be started

        # Test starting another bot type
        self.bot_manager.start_bot("oracle_bot")
        mock_oracle_bot.assert_called_once_with("Oracle Bot")
        self.assertIn("oracle_bot", self.bot_manager.threads)

        # Test invalid bot type
        with patch("builtins.print") as mocked_print:
            self.bot_manager.start_bot("unknown_bot")
            mocked_print.assert_called_with("Tipo de bot desconocido: unknown_bot")

    @patch("MinecraftAgentFramework.framework.agent_manager.threading.Thread")
    @patch("MinecraftAgentFramework.framework.agent_manager.TNTBot")
    def test_stop_bot(self, mock_tnt_bot, mock_thread):
        # Add a mock bot to threads
        mock_bot_instance = MagicMock()
        mock_thread_instance = MagicMock()
        self.bot_manager.threads["tnt_bot"] = {"bot": mock_bot_instance, "thread": mock_thread_instance}

        self.bot_manager.stop_bot("tnt_bot")
        mock_bot_instance.set_run.assert_called_once()  # Ensure set_run() is called
        mock_thread_instance.join.assert_called_once()  # Ensure thread join is called
        self.assertNotIn("tnt_bot", self.bot_manager.threads)  # Bot should be removed

        # Attempt to stop a bot that doesn't exist
        with patch("builtins.print") as mocked_print:
            self.bot_manager.stop_bot("nonexistent_bot")
            mocked_print.assert_called_with("nonexistent_bot no está en ejecución.")

    def test_list_active_bots(self):
        # Add mock bots to threads
        self.bot_manager.threads = {"bot1": {}, "bot2": {}}
        with patch("builtins.print") as mocked_print:
            self.bot_manager.list_active_bots()
            mocked_print.assert_any_call("Bots activos:")
            mocked_print.assert_any_call("- bot1")
            mocked_print.assert_any_call("- bot2")

    @patch("MinecraftAgentFramework.framework.agent_manager.BotManager.read")
    @patch("time.sleep", return_value=None)  # To avoid delays during test
    def test_read_and_response(self, mock_sleep, mock_read):
        # Simulate a start command
        mock_read.side_effect = ["start insult_bot", "stop insult_bot", "list", "exit"]
        with patch.object(self.bot_manager, "start_bot") as mock_start, \
                patch.object(self.bot_manager, "stop_bot") as mock_stop, \
                patch.object(self.bot_manager, "list_active_bots") as mock_list, \
                patch("builtins.print") as mocked_print:
            self.bot_manager.read_and_response()

            # Check commands were executed
            mock_start.assert_called_once_with("insult_bot")
            mock_stop.assert_called_once_with("insult_bot")
            mock_list.assert_called_once()
            mocked_print.assert_any_call("Saliendo del programa...")

    @patch("MinecraftAgentFramework.framework.agent_manager.mc.events.pollChatPosts")
    def test_read(self, mock_pollChatPosts):
        # Simulate no chat messages
        mock_pollChatPosts.return_value = []
        self.assertIsNone(self.bot_manager.read())

        # Simulate chat messages
        mock_pollChatPosts.return_value = [MagicMock(message="test message")]
        self.assertEqual(self.bot_manager.read(), "test message")

    @patch.object(BotManager, "start_bot")
    @patch.object(BotManager, "stop_bot")
    @patch.object(BotManager, "list_active_bots")
    def test_start_all(self, mock_list, mock_stop, mock_start):
        # Test that all available bots are started
        self.bot_manager.start_all()
        mock_start.assert_any_call("insult_bot")
        mock_start.assert_any_call("oracle_bot")
        mock_start.assert_any_call("tnt_bot")
        self.assertEqual(mock_start.call_count, 4)


if __name__ == "__main__":
    unittest.main()
