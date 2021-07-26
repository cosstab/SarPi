# TODO: import of modules will be automated on future releases
from modules.ping_module import PingModule
from modules.sarpi_default_module import SarpiDefaultModule
from chat_adapters.telegram_adapter import TelegramAdapter


# Selects the right module to analyze the received command
class SarpiDispatcher():
    def on_message(self, command: str, args: list[str]) -> str:
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
telegram.start()