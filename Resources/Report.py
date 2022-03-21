from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Class.ModelJson.Reports import Reports
from pykson import Pykson
from Class.JsonReadFile import JsonFileParser
from Class.PathFileDir import PathFileDir
from Model.Answer import Answer


class Report(Resource):
    def get(self, id_report):
        answer = Application().context.query(Answer).filter(Answer.id == id_report).first()
        file_report = answer.path_report_file

        reports = JsonFileParser(file_report).load(Reports)

        return Pykson().to_json(reports)
