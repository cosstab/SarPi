"""This is just a test of a second module"""

from events.message import SarpiMessage
from modules import SarpiModule


class PingModule(SarpiModule):
    MODULE_NAME = "Ping Module"    
    COMMAND_WORDS = ["ping"]

    def process_message(self, message: SarpiMessage):
        message.medium.reply(SarpiMessage("Pong! 🏓"))
        