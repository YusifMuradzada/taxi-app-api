from datetime import datetime

from pydantic import BaseModel


from pydantic import BaseModel, Field


class RideCreate(BaseModel):
    pickup_location: str
    destination: str

    pickup_latitude: float = Field(ge=-90, le=90)
    pickup_longitude: float = Field(ge=-180, le=180)

    distance_km: float = Field(
        gt=0,
        le=500,
    )


class RideResponse(BaseModel):
    id: int
    passenger_id: int
    driver_id: int | None
    pickup_location: str
    destination: str
    distance_km: float | None
    status: str
    price: float | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }