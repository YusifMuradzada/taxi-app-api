from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    get_current_user_id,
    require_role,
)
from app.crud.ride import create_ride, get_ride
from app.db.database import get_db
from app.models.driver import Driver
from app.models.ride import Ride
from app.schemas.ride import RideCreate, RideResponse


router = APIRouter(
    prefix="/rides",
    tags=["Rides"],
)


@router.post(
    "/",
    response_model=RideResponse,
)
def request_ride(
    ride_data: RideCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        require_role("passenger")
    ),
):
    return create_ride(
        db,
        ride_data,
        current_user_id,
    )


@router.get(
    "/available",
    response_model=list[RideResponse],
)
def get_available_rides(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        require_role("driver")
    ),
):
    driver = db.query(Driver).filter(
        Driver.user_id == current_user_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=403,
            detail="You are not a driver",
        )

    if not driver.is_available:
        raise HTTPException(
            status_code=400,
            detail="Driver is offline",
        )

    return db.query(Ride).filter(
        Ride.status == "requested",
        Ride.driver_id.is_(None),
    ).all()


@router.post(
    "/{ride_id}/accept",
    response_model=RideResponse,
)
def accept_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        require_role("driver")
    ),
):
    driver = db.query(Driver).filter(
        Driver.user_id == current_user_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=403,
            detail="You are not a driver",
        )

    if not driver.is_available:
        raise HTTPException(
            status_code=400,
            detail="Driver is offline",
        )

    ride = db.query(Ride).filter(
        Ride.id == ride_id
    ).first()

    if not ride:
        raise HTTPException(
            status_code=404,
            detail="Ride not found",
        )

    if ride.status != "requested":
        raise HTTPException(
            status_code=400,
            detail="Ride is no longer available",
        )

    if ride.driver_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Ride already has a driver",
        )

    ride.driver_id = driver.id
    ride.status = "accepted"
    driver.is_available = False

    db.commit()
    db.refresh(ride)

    return ride


@router.get(
    "/{ride_id}",
    response_model=RideResponse,
)
def get_ride_by_id(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        get_current_user_id
    ),
):
    ride = get_ride(db, ride_id)

    if not ride:
        raise HTTPException(
            status_code=404,
            detail="Ride not found",
        )

    if ride.passenger_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access this ride",
        )

    return ride


@router.post(
    "/{ride_id}/start",
    response_model=RideResponse,
)
def start_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        require_role("driver")
    ),
):
    driver = db.query(Driver).filter(
        Driver.user_id == current_user_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=403,
            detail="You are not a driver",
        )

    ride = db.query(Ride).filter(
        Ride.id == ride_id
    ).first()

    if not ride:
        raise HTTPException(
            status_code=404,
            detail="Ride not found",
        )

    if ride.driver_id != driver.id:
        raise HTTPException(
            status_code=403,
            detail="This ride is not assigned to you",
        )

    if ride.status != "accepted":
        raise HTTPException(
            status_code=400,
            detail="Ride cannot be started",
        )

    ride.status = "started"

    db.commit()
    db.refresh(ride)

    return ride


@router.post(
    "/{ride_id}/complete",
    response_model=RideResponse,
)
def complete_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        require_role("driver")
    ),
):
    driver = db.query(Driver).filter(
        Driver.user_id == current_user_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=403,
            detail="You are not a driver",
        )

    ride = db.query(Ride).filter(
        Ride.id == ride_id
    ).first()

    if not ride:
        raise HTTPException(
            status_code=404,
            detail="Ride not found",
        )

    if ride.driver_id != driver.id:
        raise HTTPException(
            status_code=403,
            detail="This ride is not assigned to you",
        )

    if ride.status != "started":
        raise HTTPException(
            status_code=400,
            detail="Ride cannot be completed",
        )

    ride.price = 2 + (ride.distance_km * 0.70)

    ride.status = "completed"
    driver.is_available = True

    db.commit()
    db.refresh(ride)

    return ride


@router.post(
    "/{ride_id}/cancel",
    response_model=RideResponse,
)
def cancel_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        require_role("passenger")
    ),
):
    ride = db.query(Ride).filter(
        Ride.id == ride_id
    ).first()

    if not ride:
        raise HTTPException(
            status_code=404,
            detail="Ride not found",
        )

    if ride.passenger_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot cancel this ride",
        )

    if ride.status not in ["requested", "accepted"]:
        raise HTTPException(
            status_code=400,
            detail="Ride cannot be cancelled",
        )

    ride.status = "cancelled"

    if ride.driver_id:
        driver = db.query(Driver).filter(
            Driver.id == ride.driver_id
        ).first()

        if driver:
            driver.is_available = True

    db.commit()
    db.refresh(ride)

    return ride


@router.get(
    "/history",
    response_model=list[RideResponse],
)
def ride_history(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        require_role("passenger")
    ),
):
    rides = db.query(Ride).filter(
        Ride.passenger_id == current_user_id
    ).order_by(
        Ride.created_at.desc()
    ).all()

    return rides


@router.get(
    "/driver/history",
    response_model=list[RideResponse],
)
def driver_ride_history(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        require_role("driver")
    ),
):
    driver = db.query(Driver).filter(
        Driver.user_id == current_user_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=403,
            detail="You are not a driver",
        )

    rides = db.query(Ride).filter(
        Ride.driver_id == driver.id
    ).order_by(
        Ride.created_at.desc()
    ).all()

    return rides