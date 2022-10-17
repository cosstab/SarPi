from collections import defaultdict
from typing import Callable
import inspect

from update import SarpiUpdate


class SarpiModuleManager():
    class CommmandManager():
        def __init__(self, command_name: str, description: str, func_qualname: str, has_params: bool,
                        func: Callable = None) -> None:
            self.command_name = command_name
            self.description = description
            self.class_name, self.func_name = func_qualname.split('.')
            self.func = func
            self.has_params = has_params
            self.params = []
    
    class PrePostcommandManager():
        def __init__(self, priority: int, func_qualname: str, func: Callable = None) -> None:
            self.priority = priority
            self.class_name, self.func_name = func_qualname.split('.')
            self.func = func
        def __repr__(self) -> str:
            return self.func_name
    
    class EventManager():
        def __init__(self, event_class: SarpiUpdate, func_qualname: str, func: Callable = None) -> None:
            self.event_class = event_class
            self.class_name, self.func_name = func_qualname.split('.')
            self.func = func
    
    command_managers: dict[str, CommmandManager] = {}
    precommand_managers: list[PrePostcommandManager] = []
    postcommand_managers: list[PrePostcommandManager] = []
    event_managers: dict[SarpiUpdate, list[EventManager]] = defaultdict(list)
    
    '''
    Python decorators are executed before module loading, so we first save the "qualname" of the decorated
    functions and, when loading modules, use them to get the function from the newly instantiated object.
    '''

    def add_command_manager(func_name: str, description: str, func_qualname: str, has_params: bool):
        command_manager = SarpiModuleManager.CommmandManager(func_name, description, func_qualname, has_params)
        SarpiModuleManager.command_managers[func_name] = command_manager
    
    def add_precommand_manager(func_qualname: str, priority: int):
        precommand_manager = SarpiModuleManager.PrePostcommandManager(priority, func_qualname)
        SarpiModuleManager.precommand_managers.append(precommand_manager)
    
    def add_postcommand_manager(func_qualname: str, priority: int):
        postcommand_manager = SarpiModuleManager.PrePostcommandManager(priority, func_qualname)
        SarpiModuleManager.postcommand_managers.append(postcommand_manager)
    
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
            
            # Search for precommand managers on the instantiated module
            for precommand_manager in self.precommand_managers:
                if precommand_manager.class_name == module.__name__:
                    # Now the module is instantiated, we can assign the precommand method to the PrePostCommandManager
                    precommand_manager.func = getattr(module_instance, precommand_manager.func_name)

                    print("\tRegistered " + precommand_manager.func_name + " precommand manager with priority "
                            + str(precommand_manager.priority))
            
            # Search for postcommand managers on the instantiated module
            for postcommand_manager in self.postcommand_managers:
                if postcommand_manager.class_name == module.__name__:
                    # Now the module is instantiated, we can assign the precommand method to the PrePostCommandManager
                    postcommand_manager.func = getattr(module_instance, postcommand_manager.func_name)

                    print("\tRegistered " + postcommand_manager.func_name + " postcommand manager with priority "
                            + str(postcommand_manager.priority))

            # Search for event managers on the instantiated module
            for event_class, event_manager_list in self.event_managers.items():
                for event_manager in event_manager_list:
                    if event_manager.class_name == module.__name__:
                        # Now the module is instantiated, we can assign the module managing method to the EventManager
                        event_manager.func = getattr(module_instance, event_manager.func_name)

                        print("\tRegistered " + event_class.__name__ + " event manager")
        
        # Sort precommands and postcommands by priority
        self.precommand_managers.sort(key=lambda precommand: precommand.priority)
        self.postcommand_managers.sort(key=lambda postcommand: postcommand.priority)

        print("Command execution order: <" + str(self.precommand_managers) + " command "
                                            +str(self.postcommand_managers) + ">")