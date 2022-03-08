from events.command import SarpiCommand
from events.message import SarpiMessage
from modules import SarpiModule
from update import SarpiUpdate
from collections import defaultdict

# Import modules
from modules import SarpiModule
from modules import *


class SarpiDispatcher():
    '''
    The dispatcher will select the right module to parse the received command from installed modules. These are
    automagically loaded on startup (they must inherit from SarpiModule and be located in modules folder to do so).
    '''

    def __init__(self) -> None:
        self.command_managers = {} #Dict of command words and managing functions
        self.event_managers = defaultdict(list)  #Dict of event classes and lists of managing functions ( dict(k,[]) )

        # Search for commands and events declared by the modules
        for module in SarpiModule.__subclasses__():
            # Use class name for module identification in case MODULE_NAME was not specified
            if module.MODULE_NAME == "":
                module.MODULE_NAME = module.__name__

            print("Loading module: " + module.MODULE_NAME)

            module_instance = module()

            # Search for command manager functions on the module that was just instantiated
            for command_name, command_func in SarpiModule.command_functions.items():
                class_name, function_name = command_func.split('.')

                if class_name == module.__name__:
                    self.command_managers[command_name] = getattr(module_instance, function_name)
                    print("\tRegistered " + command_name + " command")
            
            # Search for event manager functions on the instantiated module
            for event_class, event_func_list in SarpiModule.event_functions.items():
                for event_func in event_func_list:
                    class_name, function_name = event_func.split('.')

                    if class_name == module.__name__:
                        function = getattr(module_instance, function_name)
                        self.event_managers[event_class].append(function)
                        print("\tRegistered " + event_class.__name__ + " event manager")


    # Function to be called on every received update, which will be dispatched to the appropiate module
    def on_update(self, update: SarpiUpdate):
        print("\nNew " + update.medium.platform + " update: " + update.__class__.__name__)

        if isinstance(update, SarpiCommand):
            self._on_command(update) # Dispatch to modules asking for commands
            
        # Dispatch event to each module asking for this class of event
        try:
            for event_manager in self.event_managers[update.__class__]:
                event_manager(update)
        except KeyError:
            pass
            

    def _on_command(self, update: SarpiCommand):
            print("Command: " + update.command)
            print("Arguments: " + str(update.args))

            if (command_func := self.command_managers.get(update.command)) is not None:
                command_func(update)
            else:
                update.medium.reply(SarpiMessage("⛔ Command not found."))