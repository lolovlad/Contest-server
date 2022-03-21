from flask_restful import Resource
from Class.StartAplication import Application
from Model.Task import Task
from Class.JsonView import JsonView
import werkzeug
import datetime
from random import randint
from json import loads
import os


class Json(Resource):
    def get(self, id_task):
        tasks = Application().context.query(Task).filter(Task.id_contest == id_task).all()
        response = {
            "jsons_view": []
        }
        for task in tasks:
            file_json = task.path_test_file
            view = JsonView(file_json)
            view.generate_view()
            response["jsons_view"].append(view.view)
        return response
