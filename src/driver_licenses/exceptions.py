from src.exceptions import BadRequest, Conflict, NotFound

class DriverLicenseNotFound(NotFound):
    def __init__(self, license_id: int):
        super().__init__(detail=f"Driver license {license_id} not found")

class DriverLicenseExpired(BadRequest):
    def __init__(self, license_id: int):
        super().__init__(detail=f"Driver license {license_id} is expired")

class DriverLicenseAlreadyExists(Conflict):
    def __init__(self, license_number: str):
        super().__init__(detail=f"Driver license with number {license_number} already exists")