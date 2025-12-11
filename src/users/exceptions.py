from src.exceptions import NotFound


class UserNotFound(NotFound):
    def __init__(self):
        super().__init__(detail="User not found")
