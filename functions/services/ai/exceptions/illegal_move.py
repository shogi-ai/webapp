"""Exception for when the user tries to make an illegal move"""


class IllegalMoveException(Exception):
    """Exception for when the user tries to make an illegal move"""

    def __init__(self):
        self.message = "Move is not legal"
        super().__init__(self.message)
