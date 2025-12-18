from fastapi import FastAPI

from src.users import users_router
from src.auth import auth_router
from src.trips import trips_router
from src.cars import cars_router
from src.locations import locations_router
from src.bookings import bookings_router
from src.driver_licenses import driver_licenses_router
from src.config import config

app = FastAPI(title=config.APP_NAME)

# Include routers
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(trips_router)
app.include_router(cars_router)
app.include_router(locations_router)
app.include_router(bookings_router)
app.include_router(driver_licenses_router)

