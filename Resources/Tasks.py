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
        args["data"] = loads(args["data"])
        id_contest = Application().context.query(Contest).filter(Contest.id == id_task).first()
        task_dk = args["data"]

        name_1 = PathFileDir.create_file_name("json")
        name_2 = PathFileDir.create_file_name("py")

        name_1 = PathFileDir.abs_path(f"{name_1}")
        name_2 = PathFileDir.abs_path(f"{name_2}")

        PathFileDir.write_file(name_1, task_dk["json"])
        PathFileDir.write_file(name_2, task_dk["py"])

        task = Task(id_contest=id_contest.id,
                    time_work=task_dk["time_work"],
                    size_raw=task_dk["size_raw"],
                    type_input=task_dk["type_input"],
                    type_output=task_dk["type_output"],
                    name_test=task_dk["name_test"],
                    description=task_dk["description"],
                    description_input=task_dk["description_input"],
                    description_output=task_dk["description_output"],
                    path_test_file=f"{name_1}",
                    path_programme_file=f"{name_2}",
                    type_task=task_dk["type_task"])
        Application().context.add(task)
        Application().context.commit()
        return {"data": "ok"}

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
        task = Application().context.query(Task).filter(Task.id == id_task)
        now_task = task.first()

        os.remove(now_task.path_test_file)
        os.remove(now_task.path_programme_file)

        task.delete()
        Application().context.commit()
        return {"data": "ok"}

    def put(self, id_task):
        args = self.task_parser.parse_args()
        now_task = Application().context.query(Task).filter(Task.id == id_task).first()
        args["data"] = loads(args["data"])

        task_dk = args["data"]

        if task_dk.get("json") is not None:
            PathFileDir.write_file(now_task.path_test_file, task_dk["json"])

        if task_dk.get("py") is not None:
            PathFileDir.write_file(now_task.path_programme_file, task_dk["py"])

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