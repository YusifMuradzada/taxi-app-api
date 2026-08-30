from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )

    license_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="driver",
    )

    vehicle = relationship(
        "Vehicle",
        back_populates="driver",
        uselist=False,
    )