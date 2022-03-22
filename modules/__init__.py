from typing import Callable
import pkgutil
from module_manager import SarpiModuleManager

from update import SarpiUpdate

"""SarPi command modules must inherit from this class"""
class SarpiModule():
    MODULE_NAME = "" #Name of the module (will use class name in case it's not overriden)


    def command(description="."):
        """
        Decorator that will add a function and command description to the list of available command managers of the bot.

        The decorated function will analyze the received command (contained on a SarpiCommand object) 
        to produce (or not produce) a response.
        """

        def command_decorator(func : Callable):
            SarpiModuleManager.add_command_manager(func.__name__, description, func.__qualname__)
        
            return func
        
        return command_decorator

    def multicommand(commands_and_descriptions):
        """
        Use this decorator in case you want to manage multiple commands with only one function.
        This is useful in case you want to programatically define the list of available commands.

        Args:
            commands: list of tuples containing a command word and it's description.
        """

        def multicommand_decorator(func: Callable):
            for command, description in commands_and_descriptions:
                SarpiModuleManager.add_command_manager(command, description, func.__qualname__)

            return func
        
        return multicommand_decorator
    
    def event(event_type: SarpiUpdate):
        """
        Decorator that will add a function to the list of available event managers of the bot.

        The decorated function will analyze the received event (contained on a event object) 
        to produce (or not produce) a response.

        Args:
            event_type: Contains the class of the desired event to manage
        """

        def event_decorator(func: Callable):
            SarpiModuleManager.add_event_manager(event_type, func.__qualname__)

            return func
        
        return event_decorator


# Import every module in modules folder, except example module
__all__ = list(module_name for _, module_name, _ in pkgutil.iter_modules(["modules"]))
if "sarpi_example_module" in __all__: __all__.remove("sarpi_example_module")
