import threading
from time import sleep
import datetime
from Model.Contest import Contest

from Class.StartAplication import Application
from Resources.Login import Login
from Resources.Users import Users
from Resources.Contests import Contests
from Resources.Tasks import Tasks
from Resources.Json import Json
from Resources.Answers import Answers
from Resources.Report import Report
from Resources.Teams import Teams
from Resources.PageLoadTask import PageLoadTask
from Resources.ReportTotal import ReportTotal
from flask import Flask

from sqlalchemy.orm import Session

import os


Application().app = Flask(__name__)
app = Application().app
api = Application().api

app.config["FILE_DIR"] = os.path.dirname(os.path.abspath(__file__))

api.add_resource(Login, "/login")
api.add_resource(Users, "/users/<int:id_user>")
api.add_resource(Contests, "/contests/<int:id_contest>")
api.add_resource(Tasks, "/tasks/<int:id_task>")
api.add_resource(Json, "/json")
api.add_resource(Answers, "/answer/<int:id_task>")
api.add_resource(Report, "/report/<int:id_report>")
api.add_resource(Teams, "/teams/<int:id_team>")
api.add_resource(ReportTotal, "/report_total/<int:id_contest>")


def main():
    Application().create_context("DataBaseFiles/Contest.db")
    threading.Thread(target=switch_state_contest, daemon=True).start()
    app.run(debug=True, host="192.168.31.231", port=2000)


def switch_state_contest():
    while True:
        with Session(Application().engine) as session:
            contests = session.query(Contest).all()
            for contest in contests:
                datetime_start = contest.datetime_start
                datetime_now = datetime.datetime.now()
                if contest.datetime_start < datetime_now < contest.datetime_end:
                    contest.state_contest = 1
                elif contest.datetime_start > datetime_now:
                    contest.state_contest = 0
                else:
                    contest.state_contest = 2
            session.commit()
        sleep(10)


if __name__ == '__main__':
    main()
