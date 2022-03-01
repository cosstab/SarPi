from events.command import SarpiCommand
from events.message import SarpiMessage
from modules import SarpiModule
from update import SarpiUpdate

# Import modules
from modules import SarpiModule
from modules import *


class SarpiDispatcher():
    '''
    The dispatcher will select the right module to parse the received command from installed modules. These are
    automagically loaded on startup (they must inherit from SarpiModule and be located in modules folder to do so).
    '''

    def __init__(self) -> None:
        self.command_modules = {} #Dict of commands and SarpiModule objects
        self.event_modules = {} #Dict of events and lists of SarpiModule objects

        # Search for commands and events declared by the modules
        for module in SarpiModule.__subclasses__():
            # Use class name for module identification in case MODULE_NAME was not specified
            if module.MODULE_NAME == "":
                module.MODULE_NAME = module.__name__

            print("Loading module: " + module.MODULE_NAME)
            
            module_instance = module()
            
            for command in module.COMMAND_WORDS:
                self.command_modules[command] = module_instance
            
            for event in module.EVENTS:
                try:
                    self.event_modules[event].append(module_instance)
                except KeyError:
                    self.event_modules[event] = [module_instance]


    # Function to be called on every received update, which will be dispatched to the appropiate module
    def on_update(self, update: SarpiUpdate):
        print("\nNew " + update.medium.platform + " update: " + update.__class__.__name__)

        if isinstance(update, SarpiCommand):
            self._on_command(update) # Dispatch to modules asking for commands
            
        # Dispatch event to each module asking for this class of event
        try:
            for module in self.event_modules[update.__class__]:
                module.process_update(update)
        except KeyError:
            pass
                    

    def _on_command(self, update: SarpiCommand):
            print("Command: " + update.command)
            print("Arguments: " + str(update.args))

            command_module = self.command_modules.get(update.command)

            if command_module is not None:
                command_module.process_command(update)
            else:
                update.medium.reply(SarpiMessage("⛔ Command not found."))