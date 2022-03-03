from events.message import SarpiMessage
from modules import SarpiModule

"""
CHANGE THE NAME OF THIS FILE WHEN CREATING A NEW MODULE
Modules with this name will be ignored
"""

class SarpiExampleModule(SarpiModule):
    """
    To create a new command you need to define a new function preceded by
    "@SarpiModule.command" decorator. The name of the function will be the command
    name.

    When the command is used, the respective function will receive a SarpiCommand
    object, which you can use to get more information and create a response:

    -command.args: list of arguments after the command
    -command.command: only contains the name of the command

    Example:
        Received command: !alarm set 9 am
        command = 'alarm'
        args = ['set', '9', 'am']

    Reply to the command with 'message.medium.reply(response: SarpiMessage)'
    """

    @SarpiModule.command
    def hi(self, command):
        command.medium.reply(SarpiMessage("Hello!"))
    
    @SarpiModule.command
    def thanks(self, command):
        command.medium.reply(SarpiMessage("You're welcome :)"))
