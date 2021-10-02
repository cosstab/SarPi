from __future__ import annotations #Solution for circular dependencies when importing Message for annotations
#from message import Message
from typing import Callable
from user import User


class Medium():
    """
    Class to transfer information about where the event originated. Also contains
    functions to reply to the same medium.

    Attributes:
        platform: name of the chat platform where event originated (Telegram, Discord...).
        chat_id: unique chat identifier string among all platforms.
        user: User class object, containing information about the user who triggered the event.
            None if the event wasn't originated by an user.
    """

    def __init__(self, platform : str, chat_id : str, reply_func : Callable[[Message], None], user : User = None) -> None:
        self.platform = platform
        self.chat_id = chat_id
        self._reply_func = reply_func
        self.user = user

    def reply(self, message: Message) -> None:
        """Replies a message to the chat where the event originated"""

        self._reply_func(message)