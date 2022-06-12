from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.Team import Team
from Model.User import User
from Model.Contest import Contest
from Class.ModelJson.Team import Team as TeamJson
from pickle import dumps, loads
import json
from pykson import Pykson


class Teams(Resource):
    team_parser = reqparse.RequestParser()
    team_parser.add_argument("team", type=str)

    def get(self, id_team):
        teams = Application().context.query(Team).all() if id_team == 0 else \
            [Application().context.query(Team).filter(Team.id == id_team).first()]
        response = {
            "message": "load_team",
            "data": {"teams": []}
        }
        teams = list(map(self.__conver_team, teams))
        response["data"]["teams"] = teams
        return response

    def post(self, id_team):
        args = self.team_parser.parse_args()
        team_arg = json.loads(args["team"])
        users = []
        for user in team_arg["users"]:
            users.append(self.__get_user(user["id"]).first())
        contest = self.__get_contest(team_arg["id_contest"]).first()
        team = Team(users=users,
                    contest=contest,
                    name_team=team_arg["name_team"],
                    is_solo=team_arg["is_solo"],
                    state_contest=team_arg["state_contest"])
        Application().context.add(team)
        Application().context.commit()
        return {"message": "add_team", "data": {"massage": "запись успешно добавленны", "team": {"id": team.id}}}

    def put(self, id_team):
        args = self.team_parser.parse_args()
        team_arg = json.loads(args["team"])
        users = []
        now_team = Application().context.query(Team).filter(Team.id == team_arg["id"]).first()
        if id_team == 0:
            contest = self.__get_contest(team_arg["id_contest"]).first()
            for user in team_arg["users"]:
                users.append(self.__get_user(user["id"]).first())
            now_team.users = users
            now_team.contest = contest
            now_team.name_team = team_arg["name_team"]
            now_team.state_contest = team_arg["state_contest"]
        else:
            now_team.state_contest = team_arg["state_contest"]
        Application().context.commit()
        return {"message": "update_team", "data": "запись успешно изменена"}

    def delete(self, id_team):
        self.__get_team(id_team).delete()
        Application().context.commit()
        return {"message": "delete_team", "data": "запись успешно удалена"}

    def __get_user(self, id_user):
        try:
            user = Application().context.query(User).filter(User.id == id_user)
        except AttributeError:
            Application().context.rollback()
            user = Application().context.query(User).filter(User.id == id_user)
        return user

    def __get_contest(self, id_contest):
        try:
            contest = Application().context.query(Contest).filter(Contest.id == id_contest)
        except AttributeError:
            Application().context.rollback()
            contest = Application().context.query(Contest).filter(Contest.id == id_contest)
        return contest

    def __get_team(self, id_team):
        try:
            team = Application().context.query(Team).filter(Team.id == id_team)
        except AttributeError:
            Application().context.rollback()
            team = Application().context.query(Team).filter(Team.id == id_team)
        return team

    def __conver_team(self, team):
        users_dict = list(map(lambda x: x.__dict__, team.users))
        contest_dict = team.contest.__dict__
        team_dict = team.__dict__
        team_dict["users"] = users_dict
        team_dict["contest"] = contest_dict
        team_json = Pykson().from_json(team_dict, TeamJson, accept_unknown=True)
        return Pykson().to_dict_or_list(team_json)