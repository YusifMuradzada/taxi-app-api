
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate


def create_vehicle(
    db: Session,
    vehicle_data: VehicleCreate,
):
    vehicle = Vehicle(
        driver_id=vehicle_data.driver_id,
        brand=vehicle_data.brand,
        model=vehicle_data.model,
        color=vehicle_data.color,
        plate_number=vehicle_data.plate_number,
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle