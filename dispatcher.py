from events.command import SarpiCommand
from events.message import SarpiMessage
from update import SarpiUpdate

# Import modules
from modules import SarpiModule
from modules import *

from module_manager import SarpiModuleManager


class SarpiDispatcher():
    '''
    The dispatcher will select the right module to parse the received command from installed modules. These are
    automagically loaded on startup (they must inherit from SarpiModule and be located in modules folder to do so).
    '''

    def __init__(self) -> None:
        module_manager = SarpiModuleManager(SarpiModule)
        self.command_managers = module_manager.command_managers
        self.event_managers = module_manager.event_managers


    # Function to be called on every received update, which will be dispatched to the appropiate module
    def on_update(self, update: SarpiUpdate, **kwargs):
        print("\nNew " + update.medium.platform + " update: " + update.__class__.__name__)

        if isinstance(update, SarpiCommand):
            self._on_command(update, **kwargs) # Dispatch to modules asking for commands
            
        # Dispatch event to each module asking for this class of event
        try:
            for event_manager in self.event_managers[update.__class__]:
                event_manager.func(update)
        except KeyError:
            pass
            

    def _on_command(self, update: SarpiCommand, **kwargs):
            print("Command: " + update.command)
            print("Arguments: " + str(update.args))

            if (command_manager := self.command_managers.get(update.command)) is not None:
                command_manager.func(update, **kwargs)
            else:
                update.medium.reply(SarpiMessage("⛔ Command not found."))