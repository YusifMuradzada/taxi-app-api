
from math import radians, sin, cos, sqrt, atan2

from sqlalchemy.orm import Session

from app.models.driver import Driver


def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    R = 6371

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(d_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def find_nearest_driver(
    db: Session,
    pickup_latitude: float,
    pickup_longitude: float,
):
    drivers = db.query(Driver).filter(
        Driver.is_available == True,
        Driver.latitude.is_not(None),
        Driver.longitude.is_not(None),
    ).all()

    nearest_driver = None
    shortest_distance = float("inf")

    for driver in drivers:
        distance = calculate_distance(
            pickup_latitude,
            pickup_longitude,
            driver.latitude,
            driver.longitude,
        )

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_driver = driver

    return nearest_driver