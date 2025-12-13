from src.exceptions import NotFound

class DriverLicenseNotFound(NotFound):
    def __init__(self, license_id: int):
        super().__init__(detail=f"Driver license {license_id} not found")

class DriverLicenseExpired(NotFound):
    def __init__(self, license_id: int):
        super().__init__(detail=f"Driver license {license_id} is expired")