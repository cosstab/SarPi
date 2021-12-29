class SarpiUser():
    """
    Contains information about the user who originated an event.
    
    Attributes (not every attribute might be available on every platform):
        -id: unique identifier of the user among all platforms.
        -username: user's nickname.
        -display_name: user's displayed name.
    """

    def __init__(self, id: str, username: str = None, display_name: str = None) -> None:
        self.id = id
        self.username = username
        self.display_name = display_name