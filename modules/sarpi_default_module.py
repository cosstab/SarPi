from message import Message
from modules import SarpiModule


class SarpiDefaultModule(SarpiModule):
    MODULE_NAME = "SarPI Default Module"

    # Dictionary of commands and static responses
    __responses = {
        "hello": "🤖 Hello and welcome to the 'PI' Automated Response Service, SarPI for short.\nYou can check available commands with .list\n\n🌍Web: http://sarpi.chabal.es",
        "list": "List of available commands: hello, list, ping"
    }
    
    COMMAND_WORDS = __responses.keys()

    def process_message(self, message: Message):
        response = self.__responses.get(message.command) #Choose the appropiate command response
        message.medium.reply(Message(response))
