class RobotException(Exception):
    """Custom exception for RobotXT Parser errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return repr(self.message) 