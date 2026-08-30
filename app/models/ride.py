
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Ride(Base):
    __tablename__ = "rides"

    id: Mapped[int] = mapped_column(primary_key=True)

    passenger_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    driver_id: Mapped[int | None] = mapped_column(
        ForeignKey("drivers.id"),
        nullable=True,
    )

    pickup_location: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))

    status: Mapped[str] = mapped_column(
        String(30),
        default="requested",
    )

    price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    passenger = relationship("User")
    driver = relationship("Driver")
    
    distance_km: Mapped[float | None] = mapped_column(
    Float,
    nullable=True,
    )
    
    pickup_latitude: Mapped[float] = mapped_column(Float)
    pickup_longitude: Mapped[float] = mapped_column(Float)