from message import Message
import pkgutil

"""SarPi command modules must inherit from this class"""
class SarpiModule():
    MODULE_NAME = "" #Name of the module
    COMMAND_WORDS = [] #List of commands this module will respond to

    modules = [] #List where loaded module classes are saved

    # Subclasses will add themselves to the module dictionary
    def __init_subclass__(cls):
        print("Module loaded: " + cls.__name__)
        super().__init_subclass__()
        cls.modules.append(cls)

    def process_message(self, message: Message) -> str:
        """
        This function analyzes the received command to produce (or not) a response.

        -message.command: only contains the type of command
        -message.args: list of arguments after the command

        Example:
            Received message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']
        
        Reply to the command with 'message.medium.reply(response: Message)'
        """

# Import every module in modules folder, except example module
__all__ = list(module_name for _, module_name, _ in pkgutil.iter_modules(["modules"]))
if "sarpi_example_module" in __all__: __all__.remove("sarpi_example_module")