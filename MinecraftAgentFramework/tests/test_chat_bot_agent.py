import unittest, time, threading
from unittest.mock import MagicMock, patch
from MinecraftAgentFramework.agents.chat_bot import ChatBotAgent

class TestChatBotAgent(unittest.TestCase):
    @patch("MinecraftAgentFramework.agents.minecraft_agent.Minecraft.create")
    def setUp(self, mock_create):
        self.bot = ChatBotAgent()
        self.bot.mc = MagicMock()  # Mock Minecraft connection

    @patch("MinecraftAgentFramework.agents.minecraft_agent.Minecraft.create")
    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForCausalLM.from_pretrained")
    def test_model_loading(self, mock_model, mock_tokenizer, mock_create):
        bot = ChatBotAgent()
        mock_tokenizer.assert_called_with("facebook/opt-350m")
        mock_model.assert_called_with("facebook/opt-350m")

    @patch("agents.chat_bot.ChatBotAgent.query_llm", return_value="Hello there!")
    def test_query_llm(self, mock_query_llm):
        response = self.bot.query_llm("Hello")
        self.assertEqual(response, "Hello there!")
        mock_query_llm.assert_called_with("Hello")

    def test_read_minecraft_chat(self):
        self.bot.mc.events.pollChatPosts.return_value = [MagicMock(message="Hello, bot!", entityId=1)]
        message, sender = self.bot.read_minecraft_chat()
        self.assertEqual(message, "Hello, bot!")
        self.assertEqual(sender, 1)

    def test_send_minecraft_message(self):
        self.bot.send_minecraft_message("Testing message")
        self.bot.mc.postToChat.assert_called_with("Testing message")

    @patch("agents.chat_bot.ChatBotAgent.read_minecraft_chat", return_value=("Hello", 1))
    @patch("agents.chat_bot.ChatBotAgent.query_llm", return_value="Hi!")
    def test_run_once(self, mock_query_llm, mock_read_chat):
        # Ensure the loop runs at least once
        self.bot.running = True

        # Mock the send_minecraft_message method to avoid side effects
        with patch.object(self.bot, "send_minecraft_message") as mock_send_message:
            # Run the bot in a separate thread to avoid blocking
            def stop_bot():
                time.sleep(0.1)  # Give the loop time to execute once
                self.bot.running = False

            threading.Thread(target=stop_bot).start()
            self.bot.run()

            # Assert that the mocked methods were called
            mock_read_chat.assert_called()
            mock_query_llm.assert_called_with(
                "The following is a conversation between a player and a chatbot in Minecraft.\n"
                "Player said: Hello\nChatBot responds:"
            )
            mock_send_message.assert_called_with("Hi!")

if __name__ == "__main__":
    unittest.main()
