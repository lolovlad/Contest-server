import datetime
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from Class.StartAplication import Application


class Answer(Application().model):
    __tablename__ = "answer"

    date_send = Column(DateTime, nullable=False, default=datetime.datetime.now())
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_contest = Column(Integer, ForeignKey('Contest.id'))
    user_send = Column(Integer, ForeignKey('user.id'))
    id_task = Column(Integer, ForeignKey('task.id'))
    type_compiler = Column(Integer, nullable=False, default=1)
    total = Column(String, nullable=False, default="-")
    time = Column(String, nullable=False, default="-")
    memory_size = Column(Integer, nullable=False, default=0)
    number_test = Column(Integer, nullable=False, default=0)
    points = Column(Integer, nullable=False, default=0)

    path_report_file = Column(String, nullable=False, default="None")
    path_programme_file = Column(String, nullable=False)