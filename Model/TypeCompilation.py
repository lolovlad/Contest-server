import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from Class.StartAplication import Application


class TypeCompilation(Application().model):
    __tablename__ = "type_compilation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_compilation = Column(String, nullable=True)

