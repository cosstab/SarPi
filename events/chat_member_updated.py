from medium import SarpiMedium
from update import SarpiUpdate
from user import SarpiUser
from enum import Enum


class ChatMemberUpdated(SarpiUpdate):
    """
    Event triggered when some user (or our bot) joins or leaves a group.

    Attributes:
        update_type: indicates if the user joined or left the group.
        affected_user: the user who joined or left the group.
        is_this_bot: boolean to easily check if the affected user is the bot itself.
    
    Extra info: medium attribute includes the user who adds or kicks out the affected_user. It can
    be the affected_user himself in case he joined from a link or lefts on his own.
    """
    class UpdateType(Enum):
        USER_JOINED = 1
        USER_LEFT = 2

    def __init__(self, update_type: UpdateType, affected_user: SarpiUser, is_this_bot: bool, medium: SarpiMedium, user: SarpiUser):
        super().__init__(medium, user)
        self.update_type = update_type
        self.affected_user = affected_user
        self.is_this_bot = is_this_bot
