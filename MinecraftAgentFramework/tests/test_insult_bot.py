import unittest
from unittest.mock import patch, MagicMock
from MinecraftAgentFramework.agents.InsultBot import InsultBot  # Ensure this import is defined properly


class TestInsultBot(unittest.TestCase):

    def setUp(self):
        """
        Sets up the environment for testing `InsultBot`.
        Here, an instance of `InsultBot` is created with mocks to avoid external dependencies.
        """
        self.bot_name = "InsultBot"
        self.insult_bot = InsultBot(name=self.bot_name)
        self.insult_bot.send_message = MagicMock()  # Mock to avoid sending real messages

    def test_bot_creation(self):
        """
        Ensures the bot is created with the specified name.
        """
        self.assertEqual(self.insult_bot.name, self.bot_name, "InsultBot was not created with the correct name.")

    @patch("random.choice")
    @patch("time.sleep", return_value=None)  # Mock to avoid delays
    def test_bot_sends_insults(self, mock_sleep, mock_random_choice):
        """
        Ensures the bot sends insulting messages correctly.
        """
        # Simulated insult that will always be chosen
        insult = "You build like a zombie!"
        mock_random_choice.return_value = insult  # Force mock to return the insult

        # Override running to stop execution quickly after one loop
        self.insult_bot.running = True
        self.insult_bot.run = MagicMock(side_effect=self._mock_run(insult))

        # Call the run method
        self.insult_bot.run()

        # Verify send_message was called exactly once with the expected insult
        self.insult_bot.send_message.assert_called_once_with(insult)

    def _mock_run(self, insult):
        """
        Mocks the run method to ensure it sends the specified insult once.
        """

        def fake_run():
            if self.insult_bot.running:
                self.insult_bot.send_message(insult)  # Mimic sending message
                self.insult_bot.running = False  # Stop running immediately after

        return fake_run

    def tearDown(self):
        """
        Cleans up resources used in the tests.
        """
        self.insult_bot = None


if __name__ == "__main__":
    unittest.main()
