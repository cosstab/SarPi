from medium import Medium


class Message():
    '''
    Class to transfer text messages between SarPi's components

    Attributes:
        -text: full message
        -command: only contains the type of command
        -args: list of arguments after the command
        -medium: medium in wich the message was received. Medium class object, containing functions
            to reply to the message and info about where the messsage originated.

        Example:
            Received message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']
    '''

    def __init__(self, text: str, command: str = None, args: list[str] = None, medium: Medium = None) -> None:
        self.text = text
        self.command = command
        self.args = args
        self.medium = medium
