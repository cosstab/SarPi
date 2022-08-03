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
                # When command manager has custom parameters but they haven't been specified by the adapter,
                # we try to divide the message into the specified parameters
                if not kwargs and command_manager.has_params:
                    '''
                    ·In case there are str and int parameters, we can divide the arguments into the
                    different types of them. 
                    ·When there are only strings, each parameter will receive one word.
                    ·When there are more words than adjacent string parameters, the last parameter will receive 
                    the leftover words.
                    ·If only int parameters are specified, each one will get one int. Spare ints will
                    be ignored.
                    '''

                    def distribute_strings(param_names, kwargs, args, start_kwargs=0, start_args=0, 
                                            kwargs_end=None, args_end=None):
                        # This function distributes the words to the string parameters.
                        sliced_args = args[start_args:args_end]

                        for i in range(len(sliced_args)):
                            if i+start_kwargs+1 != len(param_names) and i != kwargs_end-1:
                                kwargs[param_names[i+start_kwargs]] = sliced_args[i]
                            else:
                                kwargs[param_names[i+start_kwargs]] = " ".join(sliced_args[i:])
                                break

                    str_detected = False
                    int_detected = False

                    for word in update.args:
                        if word.isdigit():
                            int_detected = True
                        else:
                            str_detected = True
                        
                        if int_detected and str_detected:
                            break
                    
                    param_names = []
                    for param in command_manager.params:
                        param_names.append(param.name)

                    param_idx = 0
                    word_idx = 0

                    while param_idx < len(command_manager.params):
                        param = command_manager.params[param_idx]

                        if param.annotation == int:
                            # Ignore strings at the beginning of the command when the current parameter is an int
                            while word_idx < len(update.args) and not update.args[word_idx].isdigit():
                                word_idx += 1

                            if word_idx < len(update.args):
                                kwargs[param.name] = update.args[word_idx]
                                word_idx += 1

                        elif param.annotation == str:
                            # If there are ints left, search for the end of the string fraction
                            j = len(update.args) - word_idx
                            for i, param in enumerate(command_manager.params[param_idx:]):
                                if param.annotation == int:
                                    for j in range(len(update.args[word_idx:])):
                                        if update.args[word_idx+j].isdigit():
                                            break
                                    break

                            kwargs_end = param_idx + i
                            args_end = word_idx + j
                            distribute_strings(param_names, kwargs, update.args, param_idx, word_idx, 
                                                kwargs_end, args_end)

                            word_idx = word_idx + j

                        param_idx += 1

                print("Kwargs: " + str(kwargs))
                command_manager.func(update, **kwargs)
            else:
                update.medium.reply(SarpiMessage("⛔ Command not found."))