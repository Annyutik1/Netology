import datetime
from config import DB_URI
from sqlalchemy import create_engine, select, exists, func
from sqlalchemy.orm import Session, sessionmaker
from database.model import Base, User, Match


engine = create_engine(DB_URI, echo=True)
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)


def add_user(id_vk, bdate, sex, city):
    with Session() as session:
        if session.query(exists().where(User.id_vk == id_vk)).scalar():
            session.query(User).filter(User.id_vk == id_vk).update(
                {"bdate": bdate, "sex": sex, "city": city})
        else:
            user = User(id_vk=id_vk, bdate=bdate, sex=sex, city=city,
                        create_date=datetime.datetime.now())
            session.add(user)
            session.commit()


def get_match_count(id_vk):
    with Session() as session:
        cnt = session.execute(select(func.count(Match.id_match)).join(
            User).where(User.id_vk == id_vk))
    return cnt


def add_match(id_vk, id_vk_match, photos=[]):
    with Session() as session:
        user = session.execute(select(User).where(
            User.id_vk == id_vk)).scalar()
        match = Match(user=user, id_vk_match=id_vk_match, is_showed=0,
                      photo1=(photos[0:1] or [None])[0],
                      photo2=(photos[1:2] or [None])[0],
                      photo3=(photos[2:3] or [None])[0],
                      create_date=datetime.datetime.now())
        session.add(match)
        session.commit()


def show_next_match(id_vk):
    with Session() as session:
        match = session.execute(
            select(Match).join(User).where(
                User.id_vk == id_vk).where(
                    Match.is_showed == 0).order_by(
                        Match.id_match).limit(1)).scalar()
    return match


def set_match_showed(id_match):
    with Session() as session:
        session.query(Match).filter(Match.id_match == id_match).update(
            {"is_showed": 1})
        session.commit()
