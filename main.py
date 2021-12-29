from events.message import SarpiMessage
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
        self.event_modules = {} #Dict of events and lists of SarpiModule objects

        # Search for commands and events declared by the modules
        for module in SarpiModule.modules:
            module_instance = module()
            
            for command in module.COMMAND_WORDS:
                self.command_modules[command] = module_instance
            
            for event in module.EVENTS:
                try:
                    self.event_modules[event].append(module_instance)
                except KeyError:
                    self.event_modules[event] = [module_instance]


    # Function to be called on every received update, which will be dispatched to the appropiate module
    def on_update(self, update: SarpiUpdate):
        if isinstance(update, SarpiMessage):
            self.on_command(update)
        else:
            print("\nNew " + update.medium.platform + " event: " + update.__class__.__name__)
            
            # Dispatch event to each module asking for this class of event
            for module in self.event_modules[update.__class__]:
                module.process_update(update)
                    

    def on_command(self, update: SarpiUpdate):   
            print("\nNew " + update.medium.platform + " command")
            print("Command: " + update.command)
            print("Arguments: " + str(update.args))

            command_module = self.command_modules.get(update.command)

            if command_module is not None:
                command_module.process_command(update)
            else:
                update.medium.reply(SarpiMessage("⛔ Command not found."))
        

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
