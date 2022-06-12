from Interfase.Solide import Solide
from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as orm


class Application(metaclass=Solide):
    __app = Flask("__main__")
    __api = Api(__app)
    __app.config['SECRET_KEY'] = 'def'
    __model = declarative_base()
    __context = None
    __engine = None

    @property
    def app(self):
        return self.__app

    @property
    def engine(self):
        return self.__engine

    @property
    def api(self):
        return self.__api

    @app.setter
    def app(self, val):
        self.__app = val
        self.__api = Api(self.__app)
        self.__app.config['SECRET_KEY'] = 'def'

    @property
    def context(self):
        return self.__context

    def create_context(self, file_name):
        if self.__context:
            return

        if not file_name or not file_name.strip():
            raise Exception("Необходимо указать файл базы данных.")

        name_data_base = f'sqlite:///{file_name.strip()}?check_same_thread=False'
        print(f"Подключение к базе данных по адресу {name_data_base}")

        engine = create_engine(name_data_base, echo=True)
        self.__engine = engine
        self.__context = orm.sessionmaker(bind=engine)()
        self.__model.metadata.create_all(engine)

    @property
    def model(self):
        return self.__model