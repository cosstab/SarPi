class User():
    """
    Contains information about the user who originated an event.
    
    Attributes (not every attribute might be available on every platform):
        -id: unique identifier of the user among all platforms.
        -nick: user's nickname.
        -name: user's formal name.
    """

    def __init__(self, id: str, user_name: str = None, display_name: str = None) -> None:
        self.id = id
        self.user_name = user_name
        self.display_name = display_name