from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Class.ModelJson.Reports import Reports
from pykson import Pykson
from sqlalchemy.orm import Session
from Class.JsonReadFile import JsonFileParser
from Class.PathFileDir import PathFileDir
from Model.Answer import Answer


class Report(Resource):
    def get(self, id_report):
        with Session(Application().engine) as session:
            answer = session.query(Answer).filter(Answer.id == id_report).first()
            file_report = answer.path_report_file

            reports = JsonFileParser(file_report).load(Reports)
            response = {
                "message": "load_report",
                "data": Pykson().to_json(reports)
            }
            return response
