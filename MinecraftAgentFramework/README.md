# MinecraftAgentFramework
This project provides a system to manage and interact with various bots in a Minecraft environment using Python. The bots can perform a variety of tasks, such as providing predictive responses, generating in-game effects, and more.
## Features
- Manage multiple bots in a Minecraft environment.
- Commands executed directly from the Minecraft chat.
- Supports starting, stopping, and listing active bots.
- Extensible to add more bots in the future
## Bots Included
There are three bots currently implemented in the project:
1. **InsultBot**: Generates random insults in the Minecraft chat.
2. **OracleBot**: Responds to predictive questions, like a magic 8-ball.
3. **TNTBot**: Controls explosions within the Minecraft game.

Each bot runs on a separate thread for smooth concurrent execution.
## Usage
### Running the Bot Manager
1. Import and initialize the `BotManager` class in your main Python script or interactive console:

    from agent_manager import BotManager

    manager = BotManager()
1. Use the following operations to control the bots:
    - **Start all bots**:
      manager.start_all()
- **Start a specific bot**:
  manager.start_bot("insult_bot")
- **List active bots**:
  manager.list_active_bots()
1. To enable chat-based command handling, run the following:
   manager.read_and_response()
### Chat Commands
You can control the bots directly from the Minecraft chat using simple commands:
start <bot_type>
Example: `start insult_bot`
- To stop a bot:
  list
- To exit the program:
  exit
If an invalid bot type or command is sent, you will receive an appropriate message.
## Architecture Overview
### Main Class: `BotManager`
**`BotManager`** is the core of the project, responsible for managing the lifecycle of the bots. Below are its main components:
#### Attributes:
- `threads`: A dictionary that stores information about currently active bots and their corresponding threads.

#### Methods:
1. **`start_all()`**: Starts all available bots (`InsultBot`, `OracleBot`, and `TNTBot`).
2. **`start_bot(bot_type)`**: Starts a specific bot if it's not already running.
3. **`stop_bot(bot_type)`**: Stops a specific bot that is currently active.
4. **`list_active_bots()`**: Displays a list of all currently active bots.
5. **`read()`**: Reads commands sent via the Minecraft chat.
6. **`read_and_response()`**: Continuously monitors the chat for commands and executes corresponding actions.

#### Threading
Each bot is run on its own thread using Python's threading module. This ensures smooth execution and prevents the bots from blocking each other while running.
## Bot Implementation
Each bot is implemented as part of the `MinecraftAgentFramework` module. Below is a description of the available bots:
### **InsultBot**
- **Purpose**: Sends random insults in the Minecraft chat.
- **Trigger**: Requires being started manually through a command or during `start_all()`.

### **OracleBot**
- **Purpose**: Acts as a predictive bot that responds to player questions.
- **Behavior**: Provides a response based on predefined logic.

### **TNTBot**
- **Purpose**: Controls explosions in-game by generating TNT effects.
- **Trigger**: Runs automatically when started and continuously monitors for TNT-related events.
## Example Script
Here’s an example script to demonstrate how to manage bots programmatically:
from agent_manager import BotManager

# Create an instance of BotManager
manager = BotManager()

# Start specific bots
manager.start_bot("insult_bot")
manager.start_bot("oracle_bot")

# List currently running bots
manager.list_active_bots()

# Stop a bot
manager.stop_bot("insult_bot")

# Start handling chat commands
manager.read_and_response()
## Extending the Project
### Adding New Bots
You can add additional bots by:
1. Creating a new bot class in the `MinecraftAgentFramework.agents` module.
2. Defining the logic for the new bot’s behavior (using methods such as `run()` and `set_run()`).
3. Updating the `BotManager` class to include the new bot type in its methods (`start_all`, `start_bot`, etc.).
## Dependencies
This project depends on the following Python packages:
- `MinecraftAgentFramework`: For bot integration with Minecraft.
- `threading`: For running bots concurrently.
- `time`: For handling delays in command monitoring.
## Future Enhancements
1. Add more types of bots with unique behaviors.
2. Implement logging to keep a record of bot activities.
3. Provide a graphical user interface (GUI) for bot control.
4. Add error handling for better project robustness.
5. Integrate other APIs or Minecraft mods to expand bot capabilities.