
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id"),
        unique=True,
    )
    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    color: Mapped[str] = mapped_column(String(30))
    plate_number: Mapped[str] = mapped_column(String(20), unique=True)

    driver = relationship("Driver", back_populates="vehicle")