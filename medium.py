from __future__ import annotations #Solution for circular dependencies when importing Message for annotations
#from message import SarpiMessage
from typing import Callable


class SarpiMedium():
    """
    Class to transfer information about where the event originated. Also contains
    functions to reply to the same medium.

    Attributes:
        platform: name of the chat platform where event originated (Telegram, Discord...).
        chat_id: unique chat identifier string among all platforms.
    """

    def __init__(self, platform : str, chat_id : str, reply_func : Callable[[Message], None]) -> None:
        self.platform = platform
        self.chat_id = chat_id
        self._reply_func = reply_func

    def reply(self, message: SarpiMessage) -> None:
        """Replies a message to the chat where the event originated"""

        self._reply_func(message)