from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Date, Numeric
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Publisher(Base):
    __tablename__ = "publisher"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))

    books: Mapped[List["Book"]] = relationship(back_populates="publisher")


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    id_publisher: Mapped[int] = mapped_column(ForeignKey("publisher.id"))

    publisher: Mapped[Publisher] = relationship(back_populates="books")
    stocks: Mapped[List["Stock"]] = relationship(back_populates="book")


class Shop(Base):
    __tablename__ = "shop"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))

    stocks: Mapped[List["Stock"]] = relationship(back_populates="shop")


class Stock(Base):
    __tablename__ = "stock"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(ForeignKey("book.id"))
    id_shop: Mapped[int] = mapped_column(ForeignKey("shop.id"))
    count: Mapped[int] = mapped_column(Integer)

    sales: Mapped[List["Sale"]] = relationship(back_populates="stock")
    book: Mapped[Book] = relationship(back_populates="stocks")
    shop: Mapped[Shop] = relationship(back_populates="stocks")


class Sale(Base):
    __tablename__ = "sale"
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int] = mapped_column(Numeric(6, 2))
    date_sale: Mapped[Date] = mapped_column(Date)
    id_stock: Mapped[int] = mapped_column(ForeignKey("stock.id"))
    count: Mapped[int] = mapped_column(Integer)

    stock: Mapped[Stock] = relationship(back_populates="sales")
