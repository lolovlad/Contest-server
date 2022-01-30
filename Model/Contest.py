import datetime
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, DateTime
from Class.StartAplication import Application


class Contest(Application().model):
    __tablename__ = "Contest"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_contest = Column(String, nullable=True)
    datetime_start = Column(DateTime, nullable=True)
    datetime_end = Column(DateTime, nullable=True)

    datetime_registration = Column(DateTime, default=datetime.datetime.now())

    type = Column(Integer, default=1)