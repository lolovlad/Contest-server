from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.Contest import Contest
import datetime


class Contests(Resource):
    contest_parser = reqparse.RequestParser()
    contest_parser.add_argument("id", type=int)
    contest_parser.add_argument("name_contest", type=str)
    contest_parser.add_argument("datetime_start", type=str)
    contest_parser.add_argument("datetime_end", type=str)
    contest_parser.add_argument("datetime_registration", type=str)
    contest_parser.add_argument("type", type=int)

    def get(self, id_contest):
        if id_contest == 0:
            contests = Application().context.query(Contest).all()
        else:
            contests = [Application().context.query(Contest).filter(Contest.id == id_contest).first()]
        response = {
            "contests": []
        }
        for contest in contests:
            response["contests"].append({"id": contest.id,
                                        "name_contest": contest.name_contest,
                                        "datetime_start": contest.datetime_start.strftime("%m/%d/%Y, %H:%M"),
                                        "datetime_end": contest.datetime_end.strftime("%m/%d/%Y, %H:%M"),
                                        "datetime_registration": contest.datetime_registration.strftime("%m/%d/%Y, %H:%M"),
                                        "type": contest.type})
        return response

    def post(self, id_contest):
        args = self.contest_parser.parse_args()
        contest = Contest(name_contest=args["name_contest"],
                          datetime_start=datetime.datetime.fromisoformat(args["datetime_start"]),
                          datetime_end=datetime.datetime.fromisoformat(args["datetime_end"]),
                          type=args["type"])

        Application().context.add(contest)
        Application().context.commit()
        return {"data": "ok"}

    def delete(self, id_contest):
        Application().context.query(Contest).filter(Contest.id == id_contest).delete()
        Application().context.commit()
        return {"data": "ok"}

    def put(self, id_contest):
        args = self.contest_parser.parse_args()
        now_contest = Application().context.query(Contest).filter(Contest.id == id_contest).first()
        now_contest.name_contest = args.name_contest
        now_contest.datetime_start = datetime.datetime.fromisoformat(args.datetime_start)
        now_contest.datetime_end = datetime.datetime.fromisoformat(args.datetime_end)
        now_contest.datetime_registration = datetime.datetime.now()
        now_contest.type = args.type
        Application().context.commit()
        return {"data": "ok"}
