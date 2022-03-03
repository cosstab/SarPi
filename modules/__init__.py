from events.command import SarpiCommand
from collections import defaultdict
from typing import Callable
import pkgutil

from update import SarpiUpdate

"""SarPi command modules must inherit from this class"""
class SarpiModule():
    MODULE_NAME = "" #Name of the module (will use class' name in case it's not overriden)

    command_functions = {} #Dict of command words and managing function's qualified name
    event_functions = defaultdict(list) #Dict of event classes and lists of managing function's qualified name ( dict(k,[]) )

    # USE OF THESE VARIABLES WON'T BE SUPPORTED ON FUTURE VERSIONS, DON'T USE THEM!
    COMMAND_WORDS = [] #List of commands this module will respond to
    EVENTS = [] #List of SarpiUpdate classes the module will receive instances of

    def command(func : Callable):
        """
        Decorator that will add a function to the list of available command managers of the bot.

        The decorated function will analyze the received command (contained on a SarpiCommand object) 
        to produce (or not produce) a response.
        """

        SarpiModule.command_functions[func.__name__] = func.__qualname__
        
        return func
    
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

    def process_command(self, message: SarpiCommand) -> str:
        """
        IMPLEMENTING THIS FUNCTION FOR COMMAND PROCESSING IS NOT RECOMENDED AND WILL NOT BE
        SUPPORTED IN THE FUTURE. Use decorators instead.

        This function analyzes the received command to produce (or not) a response.

        -message.command: only contains the type of command
        -message.args: list of arguments after the command

        Example:
            Received message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']
        
        Reply to the command with 'message.medium.reply(response: SarpiMessage)'
        """
    
    def process_update(self, update: SarpiUpdate):
        """
        IMPLEMENTING THIS FUNCTION FOR EVENT PROCESSING IS NOT RECOMENDED AND WILL NOT BE
        SUPPORTED IN THE FUTURE. Use decorators instead.

        This function will receive updates for events declared on EVENT list. Check events folder
        for more information on available events.
        """

# Import every module in modules folder, except example module
__all__ = list(module_name for _, module_name, _ in pkgutil.iter_modules(["modules"]))
if "sarpi_example_module" in __all__: __all__.remove("sarpi_example_module")