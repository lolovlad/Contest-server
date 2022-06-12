from flask_restful import Resource, reqparse
from Class.StartAplication import Application

from sqlalchemy.orm import Session

from sqlalchemy import func

from Model.Answer import Answer
from Model.Contest import Contest
from Model.Team import Team
from Model.User import User
from Model.Task import Task

import pickle
import os
from functools import reduce


class ReportTotal(Resource):
    report_total_parser = reqparse.RequestParser()
    report_total_parser.add_argument("state_contest", type=int)

    def get(self, id_contest):
        args = self.report_total_parser.parse_args()
        response = {
            "message": "load_report",
            "data": {"reports_total": {}}
        }
        with Session(Application().engine) as session:
            contest = session.query(Contest).filter(Contest.id == id_contest).first()

            for team in contest.teams:
                user = list(map(lambda x: f"{x.sename} {x.name} {x.secondname}", team.users))
                totals = {}
                sum_point_one = 0
                for task in contest.tasks:
                    answer_task = list(filter(lambda answer: answer.id_task == task.id, team.answers))
                    if len(answer_task) > 0:
                        answer_task = list(sorted(answer_task, key=lambda x: x.points, reverse=True))[0]
                        totals[task.id] = {"points": answer_task.points}
                        sum_point_one += answer_task.points
                    else:
                        totals[task.id] = {"points": 0}
                if response["data"]["reports_total"].get(contest.name_contest) is None:
                    response["data"]["reports_total"][contest.name_contest] = [{"name_users": ": ".join(user),
                                                                                "name_team": team.name_team,
                                                                                "total": totals,
                                                                                "sum_point": sum_point_one}]
                else:
                    response["data"]["reports_total"][contest.name_contest] += [{"name_users": ": ".join(user),
                                                                                 "name_team": team.name_team,
                                                                                 "total": totals,
                                                                                 "sum_point": sum_point_one}]
        return response





