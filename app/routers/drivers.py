from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user_id
from app.crud.driver import create_driver
from app.db.database import get_db
from app.models.driver import Driver
from app.schemas.driver import (
    DriverCreate,
    DriverLocationUpdate,
    DriverResponse,
)

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
)


@router.post(
    "/",
    response_model=DriverResponse,
)
def create(
    driver_data: DriverCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    if driver_data.user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only create your own driver profile",
        )

    return create_driver(db, driver_data)


@router.patch("/{driver_id}/online")
def go_online(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    driver = db.query(Driver).filter(
        Driver.id == driver_id,
        Driver.user_id == current_user_id,
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found",
        )

    driver.is_available = True
    db.commit()
    db.refresh(driver)

    return {"message": "Driver is now online"}


@router.patch("/{driver_id}/offline")
def go_offline(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    driver = db.query(Driver).filter(
        Driver.id == driver_id,
        Driver.user_id == current_user_id,
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found",
        )

    driver.is_available = False
    db.commit()
    db.refresh(driver)

    return {"message": "Driver is now offline"}

@router.patch("/{driver_id}/location")
def update_location(
    driver_id: int,
    location: DriverLocationUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    driver = db.query(Driver).filter(
        Driver.id == driver_id,
        Driver.user_id == current_user_id,
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found",
        )

    driver.latitude = location.latitude
    driver.longitude = location.longitude

    db.commit()
    db.refresh(driver)

    return {
        "message": "Location updated",
        "latitude": driver.latitude,
        "longitude": driver.longitude,
    }