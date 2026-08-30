
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user_id
from app.db.database import get_db
from app.models.driver import Driver
from app.models.rating import Rating
from app.models.ride import Ride
from app.schemas.rating import RatingCreate, RatingResponse


router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"],
)


@router.post(
    "/{ride_id}/driver",
    response_model=RatingResponse,
)
def rate_driver(
    ride_id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
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
            detail="You are not the passenger",
        )

    if ride.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Ride is not completed",
        )

    if not ride.driver_id:
        raise HTTPException(
            status_code=400,
            detail="Ride has no driver",
        )

    existing_rating = db.query(Rating).filter(
        Rating.ride_id == ride_id
    ).first()

    if existing_rating and existing_rating.passenger_rating:
        raise HTTPException(
            status_code=400,
            detail="Driver already rated",
        )

    if existing_rating:
        existing_rating.passenger_rating = rating_data.rating
        db.commit()
        db.refresh(existing_rating)
        return existing_rating

    new_rating = Rating(
        ride_id=ride.id,
        passenger_id=ride.passenger_id,
        driver_id=ride.driver_id,
        passenger_rating=rating_data.rating,
    )

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return new_rating


@router.post(
    "/{ride_id}/passenger",
    response_model=RatingResponse,
)
def rate_passenger(
    ride_id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
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

    if ride.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Ride is not completed",
        )

    existing_rating = db.query(Rating).filter(
        Rating.ride_id == ride_id
    ).first()

    if existing_rating and existing_rating.driver_rating:
        raise HTTPException(
            status_code=400,
            detail="Passenger already rated",
        )

    if existing_rating:
        existing_rating.driver_rating = rating_data.rating
        db.commit()
        db.refresh(existing_rating)
        return existing_rating

    new_rating = Rating(
        ride_id=ride.id,
        passenger_id=ride.passenger_id,
        driver_id=ride.driver_id,
        driver_rating=rating_data.rating,
    )

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return new_rating