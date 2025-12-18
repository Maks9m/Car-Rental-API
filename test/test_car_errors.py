import pytest
from src.cars.service import CarService
from src.cars.exceptions import CarNotFound, CarDeleteError

def test_decommission_non_existent_car(db_session):
    """Сценарій збою: видалення неіснуючої машини"""
    service = CarService()
    with pytest.raises(CarNotFound):
        service.decommission_car(db_session, car_id=999999)

def test_delete_car_with_history(db_session, setup_test_data):
    """Сценарій збою: видалення машини, у якої є поїздки"""
    service = CarService()
    # Беремо машину з поїздкою (ID 1 зазвичай має дані від seed)
    with pytest.raises(CarDeleteError):
        service.decommission_car(db_session, car_id=1)