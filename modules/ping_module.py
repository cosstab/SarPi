"""This is just a test of a second module"""

from modules import SarpiModule


class PingModule(SarpiModule):
    MODULE_NAME = "Ping Module"    
    COMMAND_WORDS = ["ping"]

    def process_message(self, command, args):
        return "Pong! 🏓"
        