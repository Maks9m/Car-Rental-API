from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from src.bookings.repository import BookingRepository
from src.trips.repository import TripRepository
from src.cars.repository import CarRepository
from src.payments.repository import PaymentRepository
from src.models import FuelType, CarModel, CarStatus, Status
from src.exceptions import BadRequest, NotFound

class TripService:
    def __init__(self):
        self.trip_repo = TripRepository()
        self.car_repo = CarRepository()
        self.payment_repo = PaymentRepository()
        self.booking_repo = BookingRepository()

    # --- 1. Simple Selects (Пошук авто) ---
    def search_available_cars(self, db: Session, location_id: int, max_price: float, fuel: FuelType):
        return self.car_repo.get_available_cars(db, location_id, max_price, fuel)

    # --- 2. Delete Scenario (Безпечне списання авто) ---
    def decommission_car(self, db: Session, car_id: int):
        # Перевірка через TripRepository (чи є історія поїздок через Booking)
        if self.trip_repo.has_car_trips(db, car_id):
            raise BadRequest(detail="Cannot delete car: history of trips exists. Use status update instead.")
        
        success = self.car_repo.hard_delete_car(db, car_id)
        if not success:
            raise NotFound(detail="Car not found")
        return {"message": f"Car {car_id} successfully deleted from the system"}

    # --- 3. Update Scenario (Зміна базової ціни моделі) ---
    def update_model_price(self, db: Session, model_id: int, new_price: Decimal):
        model = db.query(CarModel).filter(CarModel.model_id == model_id).first()
        if not model:
            raise NotFound(detail="Car model not found")
        
        model.base_price = new_price
        db.commit()
        db.refresh(model)
        return model

    # --- 4. Transaction: Finish Trip (Завершення поїздки) ---
    def finish_trip(self, db: Session, trip_id: int, end_location_id: int):
        """
        Комплексна транзакція: розрахунок вартості, оновлення статусу авто 
        та створення запису про платіж.
        """
        # 1. Знаходимо активну поїздку
        trip = self.trip_repo.get_trip_by_id(db, trip_id)
        if not trip:
            raise NotFound(detail="Trip not found")
        if trip.end_time:
            raise BadRequest(detail="Trip is already finished")

        # 2. Отримуємо дані про авто та ціну через зв'язки (Trip -> Booking -> Car -> Model)
        booking = trip.booking_rel
        if not booking or not booking.car_rel:
            raise BadRequest(detail="Trip data is inconsistent (missing booking or car)")
        
        car = booking.car_rel
        model = car.model_rel

        # 3. Розрахунок вартості (на основі часу)
        end_time = datetime.now()
        duration = end_time - trip.start_time
        
        # Рахуємо хвилини (мінімум 1 хвилина для уникнення нульової ціни)
        minutes = max(1, duration.total_seconds() / 60)
        # Припустимо, base_price — це ціна за годину. Рахуємо за хвилину:
        total_price = Decimal(minutes) * (model.base_price / Decimal(60))
        total_price = total_price.quantize(Decimal("0.01")) # Округлення до центів

        try:
            # 4. Оновлюємо поїздку
            trip.end_time = end_time
            trip.end_location = end_location_id
            trip.price = total_price

            # 5. Оновлюємо статус та локацію автомобіля
            car.status = CarStatus.AVAILABLE
            car.location = end_location_id

            self.booking_repo.complete_booking(db, booking)

            # 6. Створюємо платіж через PaymentRepository (у статусі PENDING)
            self.payment_repo.create_pending_payment(db, trip.trip_id, total_price)

            # 7. Фіналізуємо транзакцію
            db.commit()
            db.refresh(trip)
            return trip

        except Exception as e:
            db.rollback() # Скасування всіх змін у разі помилки
            raise BadRequest(detail=f"Failed to finish trip: {str(e)}")