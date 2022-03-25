from collections import defaultdict
from typing import Callable
import inspect

from update import SarpiUpdate


class SarpiModuleManager():
    command_managers = {} #Dict of command words and CommandManagers for each available command
    event_managers = defaultdict(list) #Dict of event classes and EventManagers

    class CommmandManager():
        def __init__(self, command_name: str, description: str, func_qualname: str, has_params: bool,
                        func: Callable = None) -> None:
            self.command_name = command_name
            self.description = description
            self.class_name, self.func_name = func_qualname.split('.')
            self.func = func
            self.has_params = has_params
            self.params = []
    
    class EventManager():
        def __init__(self, event_class: SarpiUpdate, func_qualname: str, func: Callable = None) -> None:
            self.event_class = event_class
            self.class_name, self.func_name = func_qualname.split('.')
            self.func = func
    
    def add_command_manager(func_name: str, description: str, func_qualname: str, has_params: bool):
        command_manager = SarpiModuleManager.CommmandManager(func_name, description, func_qualname, has_params)
        SarpiModuleManager.command_managers[func_name] = command_manager
    
    def add_event_manager(event_type: SarpiUpdate, func_qualname: str):
        event_manager = SarpiModuleManager.EventManager(event_type, func_qualname)
        SarpiModuleManager.event_managers[event_type].append(event_manager)
    
    def __init__(self, sarpi_module_class) -> None:
        # Search for commands and events declared by the modules
        for module in sarpi_module_class.__subclasses__():
            # Use class name for module identification in case MODULE_NAME was not specified
            if module.MODULE_NAME == "":
                module.MODULE_NAME = module.__name__

            print("Loading module: " + module.MODULE_NAME)

            module_instance = module()

            # Search for command managers on the module that was just instantiated
            for command_name, command_manager in self.command_managers.items():
                if command_manager.class_name == module.__name__:
                    # Now that the module is instantiated, we can assign the module managing method to the CommandManager
                    command_manager.func = getattr(module_instance, command_manager.func_name)

                    # Get list of parameters from function if it has custom parameters
                    if command_manager.has_params:
                        parameter_dict = inspect.signature(command_manager.func).parameters

                        first_param_ignored = False
                        for param_name, parameter in parameter_dict.items():
                            if first_param_ignored:
                                if parameter.annotation is inspect._empty: #Parameters are strings by default
                                    parameter = parameter.replace(annotation=str)
                                command_manager.params.append(parameter)
                            else:
                                first_param_ignored = True

                    print("\tRegistered " + command_name + " command")

            # Search for event managers on the instantiated module
            for event_class, event_manager_list in self.event_managers.items():
                for event_manager in event_manager_list:
                    if event_manager.class_name == module.__name__:
                        # Now the module is instantiated, we can assign the module managing method to the EventManager
                        event_manager.func = getattr(module_instance, event_manager.func_name)

                        print("\tRegistered " + event_class.__name__ + " event manager")