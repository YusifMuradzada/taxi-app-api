
from sqlalchemy.orm import Session

from app.models.driver import Driver
from app.schemas.driver import DriverCreate


def create_driver(
    db: Session,
    driver_data: DriverCreate,
):
    driver = Driver(
        user_id=driver_data.user_id,
        license_number=driver_data.license_number,
    )

    db.add(driver)
    db.commit()
    db.refresh(driver)

    return driver