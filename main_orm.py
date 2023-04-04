import datetime
from sqlalchemy import create_engine, select, distinct
from sqlalchemy.orm import Session
from model import Base, Publisher, Book, Shop, Stock, Sale

DB_URL = "postgresql+psycopg2://postgres:postgres@localhost/test"


def recreate_objects(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def add_test_data(session):
    publisher1 = Publisher(name="Publisher 1")
    publisher2 = Publisher(name="Publisher 2")
    book1 = Book(title="Book 1", publisher=publisher1)
    book2 = Book(title="Book 2", publisher=publisher2)
    shop1 = Shop(name="Shop 1")
    shop2 = Shop(name="Shop 2")
    stock1 = Stock(book=book1, shop=shop1, count=10)
    stock2 = Stock(book=book1, shop=shop2, count=1)
    stock3 = Stock(book=book2, shop=shop2, count=0)
    stock4 = Stock(book=book2, shop=shop2, count=1)
    sale1 = Sale(price=12.34, date_sale=datetime.date(
        2023, 1, 1), stock=stock1, count=1)
    session.add(publisher1)
    session.add(publisher2)
    session.add(book1)
    session.add(book2)
    session.add(shop1)
    session.add(shop2)
    session.add(stock1)
    session.add(stock2)
    session.add(stock3)
    session.add(stock4)
    session.add(sale1)
    session.commit()


if __name__ == "__main__":
    engine = create_engine(DB_URL)
    recreate_objects(engine)

    with Session(engine, future=True) as session:
        add_test_data(session)

        statement = select(distinct(Shop.name)).join(Stock).join(
            Book).join(Publisher).where(Stock.count > 0)

        publisher = input("Enter publisher name or id: ")
        if publisher.isdigit():
            statement = statement.where(Publisher.id == publisher)
        else:
            statement = statement.where(Publisher.name == publisher)

        result = session.execute(statement).all()
        for row in result:
            print(row[0])
