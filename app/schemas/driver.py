from pydantic import BaseModel, Field

class DriverCreate(BaseModel):
    user_id: int
    license_number: str


class DriverLocationUpdate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class DriverResponse(BaseModel):
    id: int
    user_id: int
    license_number: str
    is_available: bool
    latitude: float | None
    longitude: float | None

    model_config = {
        "from_attributes": True
    }