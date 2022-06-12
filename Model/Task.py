import datetime
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from Class.StartAplication import Application


class Task(Application().model):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_contest = Column(Integer, ForeignKey('contest.id'))
    time_work = Column(Integer, nullable=False)
    size_raw = Column(Integer, nullable=False)
    type_input = Column(Integer, nullable=False, default=1)
    type_output = Column(Integer, nullable=False, default=1)
    name_test = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    description_input = Column(String, nullable=False)
    description_output = Column(String, nullable=False)

    path_test_file = Column(String, nullable=False)

    type_task = Column(Integer, nullable=False, default=1)
    number_shipments = Column(Integer, nullable=False, default=100)

    answers = relationship("Answer", backref="task", lazy=True)