from flask_restful import Resource, reqparse
from Class.StartAplication import Application

from Model.Answer import Answer
from Model.Contest import Contest
from Model.User import User
from Model.Task import Task

from Class.PathFileDir import PathFileDir
from Class.CheckAnswer.CheckingAnswers import CreateAnswers

from json import loads
import os


class Answers(Resource):
    answer_parser = reqparse.RequestParser()
    answer_parser.add_argument("data", type=str)

    checking_answer = CreateAnswers()

    def post(self, id_task):
        args = self.answer_parser.parse_args()
        args["data"] = loads(args["data"])

        answer_deserializer = args["data"]

        task = Application().context.query(Task).filter(Task.id == id_task).first()
        contest = Application().context.query(Contest).filter(Contest.id == task.id_contest).first()
        user = Application().context.query(User).filter(User.id == answer_deserializer["user_id"]).first()

        name_file = PathFileDir.create_file_name(answer_deserializer["extension_file"])
        name_file = PathFileDir.abs_path(f"{PathFileDir.translate_name_file(user.name)}_"
                                         f"{PathFileDir.translate_name_file(user.sename)}/{name_file}")

        PathFileDir.write_file(name_file, answer_deserializer["file"])

        answer = Answer(id_contest=contest.id,
                        user_send=user.id,
                        id_task=task.id,
                        path_programme_file=str(name_file))

        Application().context.add(answer)
        Application().context.commit()

        self.checking_answer.pool_new_answer(answer)
        return {"data": "ok"}

    def get(self, id_task):
        answers = Application().context.query(Answer).filter(Answer.id_task == id_task).all()
        response = {
            "answers": []
        }
        for answer in answers:
            user = Application().context.query(User).filter(User.id == answer.user_send).first()

            response["answers"].append({
                "date_send": answer.date_send.strftime("%Y-%m-%d %H:%M:%S"),
                "id": answer.id,
                "id_contest": answer.id_contest,
                "user_send": user.name,
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

    def delete(self, id_task):
        task = Application().context.query(Task).filter(Task.id == id_task)
        now_task = task.first()
        os.remove(f"Files/{now_task.path_test_file}")
        os.remove(f"Files/{now_task.path_programme_file}")
        task.delete()
        return {"data": "ok"}

    def put(self, id_task):
        args = self.task_parser.parse_args()
        now_task = Application().context.query(Task).filter(Task.id == id_task).first()
        args["data"] = loads(args["data"])

        task_dk = args["data"]
        if task_dk.get("json") is not None:
            with open(f"Files/{now_task.path_test_file}", "w") as file:
                file.write(task_dk["json"])

        if task_dk.get("py") is not None:
            with open(f"Files/{now_task.path_programme_file}", "w") as file:
                file.write(task_dk["py"])

        now_task.time_work = task_dk["time_work"]
        now_task.size_raw = task_dk["size_raw"]
        now_task.type_input = task_dk["type_input"]
        now_task.type_output = task_dk["type_output"]
        now_task.name_test = task_dk["name_test"]
        now_task.description = task_dk["description"]
        now_task.description_input = task_dk["description_input"]
        now_task.description_output = task_dk["description_output"]

        now_task.type_task = task_dk["type_task"]

        Application().context.commit()
        return {"data": "ok"}