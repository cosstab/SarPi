from event import SarpiEvent
from message import SarpiMessage
from threading import Thread
import asyncio

# Import modules
from modules import SarpiModule
from modules import *

# Import chat adapters
from chat_adapters.telegram_adapter import TelegramAdapter
from chat_adapters.discord_adapter import DiscordAdapter
from update import SarpiUpdate


# Selects the right module to analyze the received command
class SarpiDispatcher():
    def __init__(self) -> None:
        self.command_modules = {} #Dict of commands and SarpiModule objects

        for module in SarpiModule.modules:
            module_instance = module()
            for command in module.COMMAND_WORDS:
                self.command_modules[command] = module_instance

    def on_command(self, update: SarpiUpdate) -> str:
        if isinstance(update, SarpiMessage):
            print("\nNew " + update.medium.platform + " command")
            print("Command: " + update.command)
            print("Arguments: " + str(update.args))

            command_module = self.command_modules.get(update.command)

            if command_module is not None:
                command_module.process_message(update)
            else:
                update.medium.reply(SarpiMessage("⛔ Command not found."))
                
        elif isinstance(update, SarpiEvent):
            print("\nNew " + update.medium.platform + " event")
        

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
