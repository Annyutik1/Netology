from sqlalchemy import Integer, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("id_vk", "id_vk_match"),
    )
    id_match: Mapped[int] = mapped_column(primary_key=True)
    id_vk: Mapped[int] = mapped_column(Integer)
    id_vk_match: Mapped[int] = mapped_column(Integer)
    is_showed: Mapped[int] = mapped_column(Integer, default=0)
