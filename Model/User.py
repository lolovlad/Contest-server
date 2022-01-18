import datetime
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, LargeBinary, Date, ForeignKey
from Class.StartAplication import Application
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(Application().model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, nullable=True)
    name = Column(String, nullable=True)
    sename = Column(String, nullable=True)

    type = Column(Integer, default=1)

    hashed_password = Column(String, nullable=True)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, val):
        self.hashed_password = generate_password_hash(val)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)