from flask_restful import Resource, reqparse
from Class.StartAplication import Application

from Model.Answer import Answer
from Model.Contest import Contest
from Model.Team import Team
from Model.User import User
from Model.Task import Task

from Class.PathFileDir import PathFileDir

from json import loads
import os


class PageLoadTask(Resource):
    page_load_parser = reqparse.RequestParser()
    page_load_parser.add_argument("data", type=str)

    page_load_parser.add_argument("team_id", type=int)

    def get(self, id_task):
        args = self.page_load_parser.parse_args()
        answers = Application().context.query(Answer).filter(Answer.team_send == args["team_id"]).all()

        id_contest = answers[0].id_contest
        tasks = Application().context.query(Task).filter(Task.id_contest == id_contest).all()
        answers_task = list(filter(lambda answer: answer.id_task == id_task, answers))
        response = {
            "answers": [],
            "menu": {}
        }
        for task in tasks:
            answer_task = list(filter(lambda answer: answer.id_task == task.id, answers))
            if len(answer_task) > 0:
                answer_task = list(sorted(answer_task, key=lambda x: x.points, reverse=True))[0]
                response["menu"][str(task.id)] = {"total": answer_task.total,
                                                  "points": answer_task.points}
            else:
                response["menu"][str(task.id)] = {"total": "-",
                                                  "points": 0}
        for answer in answers_task:
            user = Application().context.query(User).filter(User.id == answer.user_send).first()

            response["answers"].append({
                "date_send": answer.date_send.strftime("%Y-%m-%d %H:%M:%S"),
                "id": answer.id,
                "id_contest": answer.id_contest,
                "user_send": user.name,
                "team_send": answer.team_send,
                "id_task": answer.id_task,
                "type_compiler": answer.type_compiler,
                "total": answer.total,
                "time": answer.time,
                "memory_size": answer.memory_size,
                "number_test": answer.number_test,
                "points": answer.points,
                "path_report_file": answer.path_report_file
            })
        return response