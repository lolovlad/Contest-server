from Class.StartAplication import Application
from Resources.Login import Login
from Resources.Registration import Registration
from Resources.LoadUsers import LoadUsers
from Resources.Users import Users
from Resources.Contests import Contests
from Resources.Tasks import Tasks
from Resources.Json import Json
from Resources.Answers import Answers
from Resources.Report import Report
from flask import Flask


import os


Application().app = Flask(__name__)
app = Application().app
api = Application().api

app.config["FILE_DIR"] = os.path.dirname(os.path.abspath(__file__))

api.add_resource(Login, "/login")
api.add_resource(Registration, "/registration")
api.add_resource(LoadUsers, "/load_users")
api.add_resource(Users, "/users/<int:id_user>")
api.add_resource(Contests, "/contests/<int:id_contest>")
api.add_resource(Tasks, "/tasks/<int:id_task>")
api.add_resource(Json, "/json/<int:id_task>")
api.add_resource(Answers, "/answer/<int:id_task>")
api.add_resource(Report, "/report/<int:id_report>")


def main():
    Application().create_context("DataBaseFiles/Contest.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()
