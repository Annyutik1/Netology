from typing import List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("id_vk"),
    )
    id_user: Mapped[int] = mapped_column(primary_key=True)
    id_vk: Mapped[int] = mapped_column(Integer)
    bdate: Mapped[int] = mapped_column(Date, nullable=True)
    sex: Mapped[int] = mapped_column(Integer, nullable=True)
    city: Mapped[int] = mapped_column(String(255), nullable=True)
    create_date: Mapped[Date] = mapped_column(Date, server_default=func.now())

    matches: Mapped[List["Match"]] = relationship(back_populates="user")


class Match(Base):
    __tablename__ = "matches"
    id_match: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id_user"))
    id_vk_match: Mapped[int] = mapped_column(Integer)
    is_showed: Mapped[int] = mapped_column(Integer, default=0)
    create_date: Mapped[Date] = mapped_column(Date, server_default=func.now())
    photo1: Mapped[int] = mapped_column(String(255), nullable=True)
    photo2: Mapped[int] = mapped_column(String(255), nullable=True)
    photo3: Mapped[int] = mapped_column(String(255), nullable=True)

    user: Mapped[User] = relationship(back_populates="matches")
