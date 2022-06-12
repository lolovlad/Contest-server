import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from Class.StartAplication import Application


class Contest(Application().model):
    __tablename__ = "contest"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_contest = Column(String, nullable=True)
    datetime_start = Column(DateTime, nullable=True)
    datetime_end = Column(DateTime, nullable=True)

    datetime_registration = Column(DateTime, default=datetime.datetime.now())

    type = Column(Integer, default=1)

    state_contest = Column(Integer, default=0)

    id_type_compilation = Column(Integer, ForeignKey('type_compilation.id'), default=1)

    teams = relationship("Team", backref="contest", lazy=True)
    tasks = relationship('Task', backref='task')