from flask_restful import Resource, reqparse
from Class.StartAplication import Application

from Model.Answer import Answer
from Model.Contest import Contest
from Model.Team import Team
from Model.User import User
from Model.Task import Task

from Class.ModelJson.Answer import Answer as AnswerJson

from Class.PathFileDir import PathFileDir
from Class.CheckAnswer.CheckingAnswers import CreateAnswers

from json import loads
from pykson import Pykson
import os


class Answers(Resource):
    answer_parser = reqparse.RequestParser()
    answer_parser.add_argument("data", type=str)

    answer_parser.add_argument("id_team", type=int)
    answer_parser.add_argument("id_user", type=int)
    answer_parser.add_argument("id_contest", type=int)

    checking_answer = CreateAnswers()

    def post(self, id_task):
        args = self.answer_parser.parse_args()
        args["data"] = loads(args["data"])

        answer_deserializer = args["data"]

        task = self.__get_model(Task).filter(Task.id == id_task).first()
        team = self.__get_model(Team).filter(Team.id == answer_deserializer["id_team"]).first()
        user = self.__get_model(User).filter(User.id == answer_deserializer["id_user"]).first()

        name_file = PathFileDir.create_file_name(answer_deserializer["extension_file"])
        name_file = PathFileDir.abs_path(f"{PathFileDir.translate_name_file(user.name)}_"
                                         f"{PathFileDir.translate_name_file(user.sename)}/{name_file}")

        PathFileDir.write_file(name_file, answer_deserializer["file"])

        answer = Answer(team=team,
                        user=user,
                        task=task,
                        id_contest=task.id_contest,
                        path_programme_file=str(name_file))

        Application().context.add(answer)
        Application().context.commit()

        self.checking_answer.pool_new_answer(answer.id)
        return {"message": "add_answer", "data": "проверка началась"}

    def get(self, id_task):
        args = self.answer_parser.parse_args()
        answer = self.__get_answer()
        if id_task != 0:
            answers = answer.filter(Answer.id_task == id_task).all()
        else:
            answers = self.__filter(answer, args.id_team, args.id_user, args.id_contest)
        response = {
            "message": "load_answer",
            "data": {"answers": []}
        }
        for answer in answers:
            response["data"]["answers"].append(self.__conver_answer(answer))
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

    def __get_answer(self):
        try:
            answer = Application().context.query(Answer)
        except AttributeError:
            Application().context.rollback()
            answer = Application().context.query(Answer)
        return answer

    def __get_model(self, model):
        try:
            answer = Application().context.query(model)
        except AttributeError:
            Application().context.rollback()
            answer = Application().context.query(model)
        return answer

    def __filter(self, answers, id_team, id_user, id_contest):
        if id_team is not None:
            answers = answers.filter(Answer.id_team == id_team)
        if id_user is not None:
            answers = answers.filter(Answer.id_team == id_team)
        if id_contest is not None:
            answers = answers.filter(Answer.id_team == id_team)
        return answers.all()

    def __conver_answer(self, answer):
        try:
            user_dict = answer.user.__dict__
            team_dict = answer.team.__dict__
            task_dict = answer.task.__dict__
        except AttributeError:
            user_dict = answer.user
            team_dict = answer.team
            task_dict = answer.task
        answer_dict = answer.__dict__
        answer_dict["team"] = team_dict
        answer_dict["task"] = task_dict
        answer_dict["user"] = user_dict
        answer_json = Pykson().from_json(answer_dict, AnswerJson, accept_unknown=True)
        return Pykson().to_dict_or_list(answer_json)