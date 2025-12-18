from src.exceptions import NotFound, Conflict, BadRequest

class BookingNotFound(NotFound):
    def __init__(self, booking_id: int):
        super().__init__(detail=f"Booking {booking_id} not found")

class BookingClosed(BadRequest):
    def __init__(self, booking_id: int):
        super().__init__(detail=f"Booking {booking_id} is closed and cannot be modified")

class BookingUpdateNotAllowed(Conflict):
    def __init__(self, car_id: int):
        super().__init__(detail=f"Car {car_id} is not available for the selected dates")