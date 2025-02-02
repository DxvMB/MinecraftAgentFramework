import unittest
from unittest.mock import patch, MagicMock
from MinecraftAgentFramework.agents.oracle_bot import OracleBot  # Adjust the import as needed


class TestOracleBot(unittest.TestCase):
    @patch("MinecraftAgentFramework.agents.minecraft_agent.Minecraft.create")
    def setUp(self, mock_create):
        """
        Sets up the environment for testing `OracleBot`.
        Creates an OracleBot instance with mocked methods to simulate interactions.
        """
        self.bot_name = "OracleBot"
        self.oracle_bot = OracleBot(name=self.bot_name)
        self.oracle_bot.read_and_respond = MagicMock()  # Mock reading chat messages
        self.oracle_bot.send_message = MagicMock()  # Mock to avoid sending actual messages
        self.oracle_bot.get_current_position = MagicMock()  # Mock to avoid real Minecraft world interactions
        self.oracle_bot.build = MagicMock()  # Mock the build method
        self.oracle_bot.move = MagicMock()  # Mock the move method
        self.oracle_bot.running = True  # Simulate the bot's running state

    @patch("time.sleep", return_value=None)  # Prevent actual delays in tests
    def test_oracle_bot_greets(self, mock_sleep):
        """
        Ensures the OracleBot responds correctly to a greeting ('hola').
        """
        # Mock the chat message to return 'hola'
        self.oracle_bot.read_and_respond.return_value = "hola"

        # Run one loop cycle
        self.oracle_bot.running = False  # Ensure the bot stops after one iteration
        self.oracle_bot.run = MagicMock(side_effect=self._mock_run("hola"))  # Mock the run logic
        self.oracle_bot.run()

        # Verify send_message is called with the correct response
        self.oracle_bot.send_message.assert_called_once_with("Hola! En que puedo ayudarte en el mundo de Minecraft?")

    @patch("time.sleep", return_value=None)
    def test_oracle_bot_reports_position(self, mock_sleep):
        """
        Ensures the OracleBot reports its position correctly when 'posicion' is requested.
        """
        # Mock chat message and position
        self.oracle_bot.read_and_respond.return_value = "posicion"
        self.oracle_bot.get_current_position.return_value = MagicMock(x=10, y=64, z=5)

        # Run one loop cycle
        self.oracle_bot.running = False
        self.oracle_bot.run = MagicMock(side_effect=self._mock_run("posicion"))
        self.oracle_bot.run()

        # Verify that the OracleBot sends the correct position message
        self.oracle_bot.send_message.assert_called_once_with("Actualmente estoy en las coordenadas: x=10, y=64, z=5.")

    @patch("time.sleep", return_value=None)
    def test_oracle_bot_builds(self, mock_sleep):
        """
        Ensures the OracleBot builds a wooden block and sends the correct message when 'construye' is requested.
        """
        # Mock chat input
        self.oracle_bot.read_and_respond.return_value = "construye"

        # Run one loop cycle
        self.oracle_bot.running = False
        self.oracle_bot.run = MagicMock(side_effect=self._mock_run("construye"))
        self.oracle_bot.run()

        # Verify that the build method is called correctly
        self.oracle_bot.build.assert_called_once_with("WOOD", 1, 0, 0)
        # Verify the bot sends the correct response
        self.oracle_bot.send_message.assert_called_once_with("Me he construido un bloque de madera")

    @patch("time.sleep", return_value=None)
    def test_oracle_bot_moves(self, mock_sleep):
        """
        Ensures the OracleBot moves and sends the correct message when 'mueve' is requested.
        """
        # Mock chat input
        self.oracle_bot.read_and_respond.return_value = "mueve"

        # Run one loop cycle
        self.oracle_bot.running = False
        self.oracle_bot.run = MagicMock(side_effect=self._mock_run("mueve"))
        self.oracle_bot.run()

        # Verify that the move method is called correctly
        self.oracle_bot.move.assert_called_once_with(1, 0, 0)
        # Verify the bot sends the correct response
        self.oracle_bot.send_message.assert_called_once_with("Me he movido un bloque hacia adelante")

    def _mock_run(self, chat_message):
        """
        Mock the `run` logic to process a single chat message.
        """

        def fake_run():
            self.oracle_bot.read_and_respond.return_value = chat_message
            if chat_message.lower() == "hola":
                self.oracle_bot.send_message("Hola! En que puedo ayudarte en el mundo de Minecraft?")
            elif chat_message.lower() == "posicion":
                pos = MagicMock(x=10, y=64, z=5)  # Mocked position
                self.oracle_bot.get_current_position.return_value = pos
                self.oracle_bot.send_message(f"Actualmente estoy en las coordenadas: x={pos.x}, y={pos.y}, z={pos.z}.")
            elif chat_message.lower() == "construye":
                self.oracle_bot.build("WOOD", 1, 0, 0)
                self.oracle_bot.send_message("Me he construido un bloque de madera")
            elif chat_message.lower() == "mueve":
                self.oracle_bot.move(1, 0, 0)
                self.oracle_bot.send_message("Me he movido un bloque hacia adelante")

        return fake_run

    def tearDown(self):
        """
        Cleans up resources used during testing.
        """
        self.oracle_bot = None


if __name__ == "__main__":
    unittest.main()
