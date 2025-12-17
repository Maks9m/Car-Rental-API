from src.exceptions import NotFound

class BookingNotFound(NotFound):
    def __init__(self, booking_id: int):
        super().__init__(detail=f"Booking {booking_id} not found")