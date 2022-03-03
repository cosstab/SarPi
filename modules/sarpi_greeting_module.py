from events.chat_member_updated import ChatMemberUpdated
from events.message import SarpiMessage
from modules import SarpiModule #Import interface

"""
CHANGE THE NAME OF THIS FILE
Modules with this name will be ignored
"""

class SarpiGreetingModule(SarpiModule):
    MODULE_NAME = "SarPI Greeting Module"

    @SarpiModule.event(ChatMemberUpdated)
    def greet_new_user(self, chat_member_update: ChatMemberUpdated):
        """
        This function will be called when a ChatMemberUpdated event is generated. When a user joins
        we'll respond with a friendly greeting.
        """

        if (chat_member_update.update_type == ChatMemberUpdated.UpdateType.USER_JOINED 
                and not chat_member_update.is_this_bot):
            chat_member_update.medium.reply(SarpiMessage("Wow a new user! Welcome, "
                                                        + chat_member_update.affected_user.display_name 
                                                        + "! I'm SarPi and I'm here to help you 🤖"))
    