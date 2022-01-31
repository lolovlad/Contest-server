from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.Contest import Contest
import datetime


class Task(Resource):
    task_parser = reqparse.RequestParser()
    task_parser.add_argument("id", type=int)
    task_parser.add_argument("name_contest", type=str)
    task_parser.add_argument("datetime_start", type=str)
    task_parser.add_argument("datetime_end", type=str)
    task_parser.add_argument("datetime_registration", type=str)
    task_parser.add_argument("type", type=int)

    def post(self, id_contest):
        args = self.task_parser.parse_args()

        contest = Contest(name_contest=args["name_contest"],
                          datetime_start=datetime.datetime.fromisoformat(args["datetime_start"]),
                          datetime_end=datetime.datetime.fromisoformat(args["datetime_end"]),
                          type=args["type"])

        Application().context.add(contest)
        Application().context.commit()
        return {"data": "ok"}