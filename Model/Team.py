import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Class.StartAplication import Application


class Team(Application().model):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, autoincrement=True)
    users = relationship("User", backref="team", lazy=True)
    id_contest = Column(Integer, ForeignKey('contest.id'))
    name_team = Column(String, nullable=True)
    is_solo = Column(Boolean, nullable=False, default=True)
    state_contest = Column(Integer, nullable=False, default=1)

    answers = relationship('Answer', backref='team')
