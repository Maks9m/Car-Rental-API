from src.exceptions import Unauthorized

class UnauthorizedAction(Unauthorized):
    def __init__(self):
        super().__init__(detail="You are not authorized to perform this action")