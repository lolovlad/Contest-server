from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.Contest import Contest
from Model.TypeCompilation import TypeCompilation
from Model.Team import Team

from Class.ModelJson.Contest import Contest as ContestJson

from json import loads
import datetime
from pykson import Pykson


class Contests(Resource):
    contest_parser = reqparse.RequestParser()
    contest_parser.add_argument("id", type=int)
    contest_parser.add_argument("name_contest", type=str)
    contest_parser.add_argument("datetime_start", type=str)
    contest_parser.add_argument("datetime_end", type=str)
    contest_parser.add_argument("datetime_registration", type=str)
    contest_parser.add_argument("type", type=int)

    contest_parser.add_argument("additional_modifications", type=str)

    def get(self, id_contest):
        args = self.contest_parser.parse_args()
        args.additional_modifications = loads(args.additional_modifications)
        contest = self.__get_contest()
        if id_contest == 0:
            contests = contest.all()
            contests = self.__additional_modifications(contests, args.additional_modifications)
        else:
            contests = [contest.filter(Contest.id == id_contest).first()]
        response = {
            "message": "load_contest",
            "data": {"contests": []}
        }
        contests = list(map(self.__conver_contest, contests))
        response["data"]["contests"] = contests
        return response

    def post(self, id_contest):
        args = self.contest_parser.parse_args()
        contest = Contest(name_contest=args.name_contest,
                          datetime_start=datetime.datetime.fromisoformat(args.datetime_start),
                          datetime_end=datetime.datetime.fromisoformat(args.datetime_end),
                          type=args.type)

        Application().context.add(contest)
        Application().context.commit()
        return {"message": "add_contest", "data": "запись успешно добавленны"}

    def delete(self, id_contest):
        self.__get_contest().filter(Contest.id == id_contest).delete()
        Application().context.commit()
        return {"message": "delete_contest", "data": "запись успешно удалена"}

    def put(self, id_contest):
        args = self.contest_parser.parse_args()
        now_contest = self.__get_contest().filter(Contest.id == id_contest).first()
        now_contest.name_contest = args.name_contest
        now_contest.datetime_start = datetime.datetime.fromisoformat(args.datetime_start)
        now_contest.datetime_end = datetime.datetime.fromisoformat(args.datetime_end)
        now_contest.datetime_registration = datetime.datetime.now()
        now_contest.type = args.type
        Application().context.commit()
        return {"message": "update_contest", "data": "запись успешно изменена"}

    def __get_contest(self):
        try:
            contest = Application().context.query(Contest)
        except AttributeError:
            Application().context.rollback()
            contest = Application().context.query(Contest)
        return contest

    def __additional_modifications(self, contests, modifications):
        if modifications["type_contest"] == "solo":
            contests = list(filter(lambda x: x.type == 1, contests))
        elif modifications["type_contest"] == "team":
            contests = list(filter(lambda x: x.type in (2, 3), contests))
        if modifications["type_contest"] == "to_id_team":
            contests = list(filter(lambda x: self.__select_contest_to_team(x, modifications["id_team"]), contests))
        return contests

    def __conver_contest(self, contest):
        tasks_dict = list(map(lambda x: x.__dict__, contest.tasks))
        contest_dict = contest.__dict__
        contest_dict["tasks"] = tasks_dict
        contest_json = Pykson().from_json(contest_dict, ContestJson, accept_unknown=True)
        return Pykson().to_dict_or_list(contest_json)

    def __select_contest_to_team(self, contest, id_team):
        id_teams = [x.id for x in contest.teams]
        if int(id_team) in id_teams:
            return True
        return False

