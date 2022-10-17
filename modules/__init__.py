from typing import Callable
import pkgutil
from module_manager import SarpiModuleManager
from update import SarpiUpdate

"""SarPi command modules must inherit from this class"""
class SarpiModule():
    MODULE_NAME = "" #Name of the module (will use class name in case it's not overriden)


    def command(description=".", has_params=True):
        """
        Decorator that will add a function and command description to the list of available command managers of the bot.

        The decorated function will analyze the received command (contained on a SarpiCommand object) 
        to produce (or not produce) a response.
        """

        def command_decorator(func : Callable):
            SarpiModuleManager.add_command_manager(func.__name__, description, func.__qualname__, has_params)
        
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
                SarpiModuleManager.add_command_manager(command, description, func.__qualname__, False)

            return func
        
        return multicommand_decorator

    def precommand(priority: int = 1000):
        '''
        Functions using this decorator will be executed before every command.

        A priority number can be specified. In case there are multiple precommands, the one with the
        lower number will be executed first. The priority number must be between 0 and 1000, both included.

        Precommands can return return False to stop the rest of the command execution chain. 
        '''

        if not (0 <= priority <= 1000):
            raise ValueError

        def precommand_decorator(func : Callable):
            SarpiModuleManager.add_precommand_manager(func.__qualname__, priority)
        
            return func
        
        return precommand_decorator
    
    def postcommand(priority: int = 1000):
        '''
        Same as precommand, but functions decorated by this decorator will be executed AFTER every command.

        Returning False will stop the execution of the postcommmands with lower priority (higher priority
        number).

        A command can pass an object to postcommands by returning it.
        '''

        if not (0 <= priority <= 1000):
            raise ValueError

        def postcommand_decorator(func : Callable):
            SarpiModuleManager.add_postcommand_manager(func.__qualname__, priority)
        
            return func
        
        return postcommand_decorator
    
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
