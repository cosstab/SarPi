from sarpi_module import SarpiModule #Import interface


class SarpiExampleModule(SarpiModule):
    MODULE_NAME = "Example Module" #The name of your module
    COMMAND_WORDS = ["hello", "list"] #List of commands this module will respond to

    def process_message(self, command, args):
        """
        This function analyzes the received command and returns a response.

        -command: only contains the type of command
        -args: list of arguments after the command

        Example:
            Message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']

        In this case we won't check the arguments.
        """

        if (command == "hello"):
            return "Hello!"
        elif (command == "list"):
            return ("List of available commands:"
                    "hello"
                    "list")
    