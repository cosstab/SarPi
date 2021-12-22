from medium import SarpiMedium
from update import SarpiUpdate
from user import SarpiUser


class SarpiMessage(SarpiUpdate):
    '''
    Class to transfer text messages between SarPi's components

    Attributes:
        -text: full message
        -command: only contains the type of command
        -args: list of arguments after the command

        Example:
            Received message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']
    '''

    def __init__(self, text: str, command: str = None, args: list[str] = None, medium: SarpiMedium = None, user: SarpiUser = None) -> None:
        super().__init__(medium, user)
        self.text = text
        self.command = command
        self.args = args
