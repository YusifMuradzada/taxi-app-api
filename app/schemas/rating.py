
from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    rating: int = Field(
        ge=1,
        le=5,
    )


class RatingResponse(BaseModel):
    id: int
    ride_id: int
    passenger_id: int
    driver_id: int
    passenger_rating: int | None
    driver_rating: int | None

    model_config = {
        "from_attributes": True
    }