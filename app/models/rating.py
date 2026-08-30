
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True)

    ride_id: Mapped[int] = mapped_column(
        ForeignKey("rides.id"),
        unique=True,
    )

    passenger_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id")
    )

    passenger_rating: Mapped[int | None] = mapped_column(
        nullable=True
    )

    driver_rating: Mapped[int | None] = mapped_column(
        nullable=True
    )