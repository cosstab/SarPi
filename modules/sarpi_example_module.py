from modules import SarpiModule #Import interface


class SarpiExampleModule(SarpiModule):
    MODULE_NAME = "Example Module" #The name of your module
    COMMAND_WORDS = ["hello", "list"] #List of commands this module will respond to

    def process_message(self, message):
        """
        This function analyzes the received command and returns a response.

        -message.command: only contains the type of command
        -message.args: list of arguments after the command

        Example:
            Received message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']

        In this case we won't check the arguments.
        """

        if (message.command == "hello"):
            return "Hello!"
        elif (message.command == "list"):
            return ("List of available commands:"
                    "hello"
                    "list")
    