
from pydantic import BaseModel


class VehicleCreate(BaseModel):
    driver_id: int
    brand: str
    model: str
    color: str
    plate_number: str


class VehicleResponse(BaseModel):
    id: int
    driver_id: int
    brand: str
    model: str
    color: str
    plate_number: str

    model_config = {
        "from_attributes": True
    }