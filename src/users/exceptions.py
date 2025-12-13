from src.exceptions import NotFound, Conflict


class UserNotFound(NotFound):
    def __init__(self, user_id: int):
        super().__init__(detail=f"User {user_id} not found")

class DuplicateEmail(Conflict):
    def __init__(self, email: str):
        super().__init__(detail=f"Duplicate email: {email}")