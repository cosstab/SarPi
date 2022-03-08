from events.command import SarpiCommand
from events.message import SarpiMessage
from modules import SarpiModule


class SarpiDefaultModule(SarpiModule):
    MODULE_NAME = "SarPI Default Module"

    # Dictionary of commands and static responses
    __responses = {
        "hello": "🤖 Hello and welcome to the 'PI' Automated Response Service, SarPI for short.\nYou can check available commands with 'list'\n\n🌍Web: http://sarpi.chabal.es",
        "ping": "Pong! 🏓",
        "list": ""
    }

    def get_commands(self):
        command_list = []
        response = ""

        # Get commands from every installed module
        for command_func in self.command_functions:
            command_list.append(command_func)
        
        command_list.sort()
        
        # Format response
        for command in command_list:
            response += "·" + command + "\n"

        return response

    @SarpiModule.multicommand(__responses.keys())
    def process_command(self, message: SarpiCommand):
        if (message.command == "list"):
            response = "List of available commands:\n" + self.get_commands() #List available commands
        else:
            response = self.__responses.get(message.command) #Choose the appropiate command response

        message.medium.reply(SarpiMessage(response))
