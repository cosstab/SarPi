from medium import SarpiMedium
from update import SarpiUpdate
from user import SarpiUser


class SarpiMessage(SarpiUpdate):
    '''
    Class to transfer text messages between SarPi's components

    Attributes:
        -text: full message
    '''

    def __init__(self, text: str, medium: SarpiMedium = None, user: SarpiUser = None) -> None:
        super().__init__(medium, user)
        self.text = text
