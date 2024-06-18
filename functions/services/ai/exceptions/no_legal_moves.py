"""Exception for when there are no move valid moves"""


class NoMovesException(Exception):
    """Exception for when there are no move valid moves"""

    def __init__(self):
        self.message = "No legal moved could be found"
        super().__init__(self.message)
