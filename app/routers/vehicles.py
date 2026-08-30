from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user_id
from app.crud.vehicle import create_vehicle
from app.db.database import get_db
from app.models.driver import Driver
from app.schemas.vehicle import VehicleCreate, VehicleResponse


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
)


@router.post(
    "/",
    response_model=VehicleResponse,
)
def create(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    driver = db.query(Driver).filter(
        Driver.id == vehicle_data.driver_id,
        Driver.user_id == current_user_id,
    ).first()

    if not driver:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="You can only add a vehicle to your own driver profile",
        )

    return create_vehicle(db, vehicle_data)