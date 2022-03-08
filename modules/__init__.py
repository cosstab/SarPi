from events.command import SarpiCommand
from collections import defaultdict
from typing import Callable
import pkgutil

from update import SarpiUpdate

"""SarPi command modules must inherit from this class"""
class SarpiModule():
    MODULE_NAME = "" #Name of the module (will use class' name in case it's not overriden)

    command_functions = {} #Dict of command words and managing function's qualified names
    event_functions = defaultdict(list) #Dict of event classes and lists of managing function's qualified name ( dict(k,[]) )


    def command(func : Callable):
        """
        Decorator that will add a function to the list of available command managers of the bot.

        The decorated function will analyze the received command (contained on a SarpiCommand object) 
        to produce (or not produce) a response.
        """

        SarpiModule.command_functions[func.__name__] = func.__qualname__
        
        return func

    def multicommand(commands):
        """
        Use this decorator in case you want to manage multiple commands with only one function.
        This is useful in case you want to programatically define the list of available commands.

        Args:
            commands: list of command words the decorated function will manage.
        """

        def multicommand_decorator(func: Callable):
            for command in commands:
                SarpiModule.command_functions[command] = func.__qualname__

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
            SarpiModule.event_functions[event_type].append(func.__qualname__)

            return func
        
        return event_decorator


# Import every module in modules folder, except example module
__all__ = list(module_name for _, module_name, _ in pkgutil.iter_modules(["modules"]))
if "sarpi_example_module" in __all__: __all__.remove("sarpi_example_module")
