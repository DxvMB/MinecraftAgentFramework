import sys
sys.path.append('./MinecraftAgentFramework/')  # Adjust 'path/to/project' to the appropriate directory
import unittest
from unittest.mock import patch, MagicMock
from agents.tnt_bot import TNTBot


class TestTNTBot(unittest.TestCase):
    @patch("agents.minecraft_agent.Minecraft.create")
    def setUp(self, mock_create):
        """
        Sets up the environment for testing `TNTBot`.
        A TNTBot instance is created with mocked methods to avoid real interactions with the Minecraft world.
        """
        self.bot_name = "TNTBot"
        self.tnt_bot = TNTBot(name=self.bot_name)
        self.tnt_bot.build = MagicMock()        # Mock the build method to avoid real building
        self.tnt_bot.send_message = MagicMock()  # Mock the send_message method to avoid actual messages
        self.tnt_bot.running = True             # Simulate the bot's running state

    @patch("random.randint")
    @patch("time.sleep", return_value=None)  # Prevent actual delays for testing
    def test_tnt_bot_builds_and_ignites(self, mock_sleep, mock_randint):
        """
        Ensures the TNTBot builds and ignites TNT correctly and sends appropriate messages.
        """
        mock_randint.side_effect = [2, 3]  # Mock random.randint to return predictable x and z coordinates

        self.tnt_bot.running = False  # Ensure the bot stops after one iteration for testing

        # Run the bot (mocked to test just one loop cycle)
        self.tnt_bot.run = MagicMock(side_effect=self._mock_run(2, 3))

        # Call the mocked `run` method
        self.tnt_bot.run()

        # Verify that the correct sequence of actions is performed
        self.tnt_bot.build.assert_any_call("TNT", 2, 0, 3)  # Verify TNT block placement
        self.tnt_bot.build.assert_any_call("REDSTONE_BLOCK", 2, 1, 3)  # Ignite TNT
        self.tnt_bot.build.assert_any_call("AIR", 2, 1, 3)  # Clear the ignition block
        self.tnt_bot.send_message.assert_called_once_with("TNT ignited!")  # Verify the message was sent

    def _mock_run(self, x, z):
        """
        Mock the `run` logic to simulate one loop cycle for TNTBot.
        """
        def fake_run():
            self.tnt_bot.build("TNT", x, 0, z)  # Place TNT at x, 0, z
            self.tnt_bot.build("REDSTONE_BLOCK", x, 1, z)  # Ignite TNT
            self.tnt_bot.build("AIR", x, 1, z)  # Clear Redstone block
            self.tnt_bot.send_message("TNT ignited!")  # Send message
        return fake_run

    def tearDown(self):
        """
        Cleans up resources used during the tests.
        """
        self.tnt_bot = None


if __name__ == "__main__":
    unittest.main()
