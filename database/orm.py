from config import DB_URI
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session, sessionmaker
from database.model import Base, Match


engine = create_engine(DB_URI)
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)


def get_match_count(id_vk):
    with Session() as session:
        cnt = session.execute(
            select(func.count(Match.id_match)).where(Match.id_vk == id_vk))
    return cnt


def add_match(id_vk, id_vk_match):
    with Session() as session:
        match = Match(id_vk=id_vk, id_vk_match=id_vk_match, is_showed=0)
        session.add(match)
        session.commit()


def show_next_match(id_vk):
    with Session() as session:
        match = session.execute(
            select(Match).where(
                Match.id_vk == id_vk).where(
                    Match.is_showed == 0).order_by(
                        Match.id_match).limit(1)).scalar()
    return match


def set_match_showed(id_match):
    with Session() as session:
        session.query(Match).filter(Match.id_match == id_match).update(
            {"is_showed": 1})
        session.commit()
