class SarpiMessage():
    '''
    Class to transfer received messages between SarPi's components

    Attributes:

        -command: only contains the type of command
        -args: list of arguments after the command
        -medium: medium in wich the message was received. Object of [TBD], containing functions to reply to the message.

        Example:
            Received message: !alarm set 9 am
            command = 'alarm'
            args = ['set', '9', 'am']
    '''

    def __init__(self, command: str, args: list[str], medium: "TBD") -> None:
        self.command = command
        self.args = args
        self.medium = medium
