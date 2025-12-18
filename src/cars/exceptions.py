from src.exceptions import NotFound, BadRequest

class CarNotFound(NotFound):
    def __init__(self, detail: str = "Car not found or ID is invalid"):
        super().__init__(detail=detail)

class ModelNotFound(NotFound):
    def __init__(self, detail: str = "Car model not found"):
        super().__init__(detail=detail)

class CarDeleteError(BadRequest):
    def __init__(self, detail: str = "Cannot delete car: history of trips exists."):
        super().__init__(detail=detail)