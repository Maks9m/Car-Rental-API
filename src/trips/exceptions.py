from src.exceptions import NotFound, BadRequest

class TripNotFound(NotFound):
    def __init__(self, detail: str = "Trip not found"):
        super().__init__(detail=detail)

class TripAlreadyFinished(BadRequest):
    def __init__(self, detail: str = "This trip is already completed"):
        super().__init__(detail=detail)

class TripTransactionError(BadRequest):
    def __init__(self, error_message: str):
        super().__init__(detail=f"Failed to finish trip: {error_message}")