from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.Contest import Contest


class SwitchStateContest(Resource):
    switch_state_contest_parser = reqparse.RequestParser()
    switch_state_contest_parser.add_argument("data", type=str)

    def put(self, id_contest):
        args = self.switch_state_contest_parser.parse_args()
        contest = Application().context.query(Contest).filter(Contest.id == id_contest).first()
        contest.state_contest = args["state_contest"]
        return {"data": "ok"}