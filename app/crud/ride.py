from sqlalchemy.orm import Session

from app.models.ride import Ride
from app.schemas.ride import RideCreate
from app.services.ride_service import find_nearest_driver


def create_ride(
    db: Session,
    ride_data: RideCreate,
    passenger_id: int,
):
    driver = find_nearest_driver(
        db,
        ride_data.pickup_latitude,
        ride_data.pickup_longitude,
    )

    ride = Ride(
        passenger_id=passenger_id,
        driver_id=driver.id if driver else None,
        pickup_location=ride_data.pickup_location,
        destination=ride_data.destination,
        pickup_latitude=ride_data.pickup_latitude,
        pickup_longitude=ride_data.pickup_longitude,
        distance_km=ride_data.distance_km,
        status="requested",
    )

    db.add(ride)
    db.commit()
    db.refresh(ride)

    return ride


def get_ride(
    db: Session,
    ride_id: int,
):
    return db.query(Ride).filter(
        Ride.id == ride_id
    ).first()