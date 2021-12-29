from events.message import SarpiMessage
from medium import SarpiMedium
from user import SarpiUser


class SarpiCommand(SarpiMessage):
    '''
    Class containing a received command, inherates from SarpiMessage.

    Attributes:
        -command: only contains the type of command 
        -args: list of arguments after the command 

        Example:
            Received message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']
    '''

    def __init__(self, text: str, command: str = None, args: list[str] = None, medium: SarpiMedium = None, user: SarpiUser = None) -> None:
        super().__init__(text, medium, user)
        self.command = command
        self.args = args
