from threading import Thread
import asyncio

# TODO: import of modules will be automated on future releases
from modules.ping_module import PingModule
from modules.sarpi_default_module import SarpiDefaultModule

# Chat adapters
from chat_adapters.telegram_adapter import TelegramAdapter
from chat_adapters.discord_adapter import DiscordAdapter


# Selects the right module to analyze the received command
class SarpiDispatcher():
    def on_command(self, command: str, args: list[str]) -> str:
        print("Command: " + command)
        print("Arguments: " + str(args))

        # TODO: automate module instantiation and command dispatch
        default_module = SarpiDefaultModule()
        ping_module = PingModule()

        if command in default_module.COMMAND_WORDS:
            return default_module.process_message(command, args)
        elif command in ping_module.COMMAND_WORDS:
            return ping_module.process_message(command, args)
        else:
            return "⛔ Command not found."

sarpi_dispatcher = SarpiDispatcher()

# Instantiate chat adapters and indicate the dispatcher
telegram = TelegramAdapter(sarpi_dispatcher)
discord = DiscordAdapter(sarpi_dispatcher)

# Start chat adapters on new threads
# Telegram
telegram_thread = Thread(target = telegram.start, args = ())
telegram_thread.start()

# Discord
asyncio.get_child_watcher()
loop = asyncio.get_event_loop()
loop.create_task(discord.start())
discord_thread = Thread(target=loop.run_forever)
discord_thread.start()

# Wait until every adapter finished it's execution
telegram_thread.join()
discord_thread.join()
