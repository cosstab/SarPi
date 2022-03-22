from events.command import SarpiCommand
from events.message import SarpiMessage
from module_manager import SarpiModuleManager
from modules import SarpiModule


class SarpiDefaultModule(SarpiModule):
    MODULE_NAME = "SarPI Default Module"

    # Dictionary of commands and static responses
    __responses = {
        "hello": ("🤖 Hello and welcome to the 'PI' Automated Response Service, SarPI for short.\nYou can check available commands with 'list'\n\n🌍Web: http://sarpi.chabal.es",
                        "Receive a welcome message"),
        "ping": ("Pong! 🏓", "Check if bot is working"),
        "list": ("", "List all available messages")
    }

    def get_commands_and_descriptions(responses):
        commands_and_descriptions = []

        for command, response_and_description in responses.items():
            commands_and_descriptions.append((command, response_and_description[1]))
        
        return commands_and_descriptions

    def get_bot_commands(self):
        command_list = []
        response = ""

        # Get commands from every installed module
        for command_func in SarpiModuleManager.command_managers:
            command_list.append(command_func)
        
        command_list.sort()
        
        # Format response
        for command in command_list:
            response += "·" + command + "\n"

        return response

    @SarpiModule.multicommand(get_commands_and_descriptions(__responses))
    def process_command(self, message: SarpiCommand):
        if (message.command == "list"):
            response = "List of available commands:\n" + self.get_bot_commands() #List available commands
        else:
            response = self.__responses.get(message.command)[0] #Choose the appropiate command response

        message.medium.reply(SarpiMessage(response))
