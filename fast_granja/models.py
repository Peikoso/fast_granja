from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class ChickenDeathReasonModel:
    __tablename__ = "chicken_death_reason"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    reason: Mapped[str] = mapped_column(unique=True)


@table_registry.mapped_as_dataclass
class ChickenRaceModel:
    __tablename__ = "chicken_race"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    race: Mapped[str] = mapped_column(unique=True)


@table_registry.mapped_as_dataclass
class UserModel:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    full_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    isAdmin: Mapped[bool]


@table_registry.mapped_as_dataclass
class FlockModel:
    __tablename__ = "flock"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    price: Mapped[int]
    amount: Mapped[int]
    arrival_date: Mapped[date]
    supplier_name: Mapped[str]
    isactive: Mapped[bool]
    flock_name: Mapped[str] = mapped_column(unique=True)

    race_id: Mapped[int] = mapped_column(
        ForeignKey("chicken_race.id", ondelete="RESTRICT")
    )

    daily_eggs: Mapped[list["DailyEggsModel"]] = relationship(
        init=False, lazy="selectin", cascade="all, delete"
    )
    chicken_death: Mapped[list["ChickenDeathModel"]] = relationship(
        init=False, lazy="selectin", cascade="all, delete"
    )


@table_registry.mapped_as_dataclass
class DailyEggsModel:
    __tablename__ = "daily_eggs"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    total_eggs: Mapped[int]
    broken_eggs: Mapped[int]
    day: Mapped[date]

    flock_id: Mapped[int] = mapped_column(ForeignKey("flock.id", ondelete="CASCADE"))


@table_registry.mapped_as_dataclass
class ChickenDeathModel:
    __tablename__ = "chicken_death"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    amount: Mapped[int]
    day: Mapped[date]

    reason_id: Mapped[int] = mapped_column(
        ForeignKey("chicken_death_reason.id", ondelete="RESTRICT")
    )
    flock_id: Mapped[int] = mapped_column(ForeignKey("flock.id", ondelete="CASCADE"))
