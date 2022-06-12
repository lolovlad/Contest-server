from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.Contest import Contest
from Model.Task import Task
from Class.PathFileDir import PathFileDir
import werkzeug
import datetime
from random import randint
from json import loads
import os


class Tasks(Resource):
    task_parser = reqparse.RequestParser()
    task_parser.add_argument("data", type=str)

    def post(self, id_task):
        args = self.task_parser.parse_args()
        task_dk = loads(args["data"])

        contest = self.__get_contest().filter(Contest.id == task_dk["id_contest"]).first()

        name_1 = PathFileDir.create_file_name("json")

        name_1 = PathFileDir.abs_path(f"{name_1}")
        PathFileDir.write_file(name_1, task_dk["json"])

        task = Task(time_work=task_dk["time_work"],
                    size_raw=task_dk["size_raw"],
                    type_input=task_dk["type_input"],
                    type_output=task_dk["type_output"],
                    name_test=task_dk["name_test"],
                    description=task_dk["description"],
                    description_input=task_dk["description_input"],
                    description_output=task_dk["description_output"],
                    path_test_file=f"{name_1}",
                    type_task=task_dk["type_task"])
        contest.tasks.append(task)
        Application().context.commit()
        return {"message": "add_task", "data": {"massage": "запись успешно добавленны", "task": {"id": task.id}}}

    def get(self, id_task):
        tasks = Application().context.query(Task).filter(Task.id_contest == id_task).all()
        response = {
            "tasks": []
        }
        for task in tasks:
            response["tasks"].append({"id": task.id,
                                      "time_work": task.time_work,
                                      "size_raw": task.size_raw,
                                      "type_input": task.type_input,
                                      "type_output": task.type_output,
                                      "name_test": task.name_test,
                                      "description": task.description,
                                      "description_input": task.description_input,
                                      "description_output": task.description_output,
                                      "path_test_file": task.path_test_file,
                                      "path_programme_file": task.path_programme_file,
                                      "type_task": task.type_task,
                                      "number_shipments": task.number_shipments})
        return response

    def delete(self, id_task):
        self.__get_task().filter(Task.id == id_task).delete()
        Application().context.commit()
        return {"message": "delete_task", "data": "запись успешно удалена"}

    def put(self, id_task):
        args = self.task_parser.parse_args()
        task_dk = loads(args["data"])
        now_task = self.__get_task().filter(Task.id == task_dk["id"]).first()

        if task_dk.get("json") is not None:
            PathFileDir.write_file(now_task.path_test_file, task_dk["json"])

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
        return {"message": "update_task", "data": "запись успешно изменена"}

    def __get_contest(self):
        try:
            contest = Application().context.query(Contest)
        except AttributeError:
            Application().context.rollback()
            contest = Application().context.query(Contest)
        return contest

    def __get_task(self):
        try:
            task = Application().context.query(Task)
        except AttributeError:
            Application().context.rollback()
            task = Application().context.query(Task)
        return task