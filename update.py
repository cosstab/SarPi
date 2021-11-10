from medium import SarpiMedium
from user import SarpiUser


class SarpiUpdate():
    '''
    Parent class of the different chat updates SarPi can manage.

    Attributes: 
        user: User class object, containing information about the user who triggered the update.
            None if the event wasn't originated by an user.
        medium: medium in wich the update was received. SarpiMedium class object, containing functions
            to reply to the message and info about where the messsage originated.
    '''
    
    def __init__(self, medium: SarpiMedium, user: SarpiUser = None):
        self.medium = medium
        self.user = user
