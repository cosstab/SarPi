from events.message import SarpiMessage
from modules import SarpiModule #Import interface

"""
CHANGE THE NAME OF THIS FILE
Modules with this name will be ignored
"""

class SarpiExampleModule(SarpiModule):
    MODULE_NAME = "Example Module" #The name of your module
    COMMAND_WORDS = ["hi", "thanks"] #List of commands this module will respond to

    def process_command(self, message: SarpiMessage):
        """
        This function analyzes the received command and returns a response.

        -message.command: only contains the type of command
        -message.args: list of arguments after the command

        Example:
            Received message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']

        In this case we won't check the arguments.
        Reply to the command with 'message.medium.reply(response: SarpiMessage)'
        """

        if (message.command == "hi"):
            message.medium.reply(SarpiMessage("Hello!"))
        elif (message.command == "thanks"):
            message.medium.reply(SarpiMessage("You're welcome :)"))
    