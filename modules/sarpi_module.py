"""Interface to be implemented by SarPi command modules"""
class SarpiModule():
    MODULE_NAME = "" #Name of the module
    COMMAND_WORDS = [] #List of commands this module will respond to

    def process_message(self, command: str, args: list[str]) -> str:
        """
        This function analyzes the received command and returns a response.

        -command: only contains the type of command
        -args: list of arguments after the command

        Example:
            Message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']
        """