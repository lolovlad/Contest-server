from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.User import User
from Model.Team import Team
from Class.ModelJson.User import User as UserJson
from pykson import Pykson


class Users(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument("type", type=int)
    user_parser.add_argument("name", type=str)
    user_parser.add_argument("sename", type=str)
    user_parser.add_argument("secondname", type=str)
    user_parser.add_argument("login", type=str)
    user_parser.add_argument("password", type=str)

    def get(self, id_user):
        #users = list(map(self.__is_team, self.__get_user_all()))
        users = self.__get_user_all()
        data = {
            "message": "load_user",
            "data": {"users": list(map(self.__conver_user, users))}
        }
        return data

    def post(self, id_user):
        args = self.user_parser.parse_args()
        if self.__is_login(args):
            return {"message": "error", "data": "Такой логин уже существует"}
        user = User(name=args.name,
                    sename=args.sename,
                    secondname=args.secondname,
                    login=args.login,
                    type=args.type)
        user.password = args.password
        Application().context.add(user)
        Application().context.commit()
        return {"message": "add_user", "data": "запись успешно добавленна"}

    def put(self, id_user):
        args = self.user_parser.parse_args()
        now_user = self.__get_filter_user(id_user).first()
        now_user.login = args.login
        now_user.name = args.name
        now_user.sename = args.sename
        now_user.type = args.type
        if len(args.password) > 0:
            now_user.password = args.password
        Application().context.commit()
        return {"message": "add_user", "data": "запись успешно обновленна"}

    def delete(self, id_user):
        self.__get_filter_user(id_user).delete()
        Application().context.commit()
        return {"message": "add_user", "data": "запись успешно удалена"}

    def __get_user_all(self):
        try:
            users = Application().context.query(User).all()
        except AttributeError:
            Application().context.rollback()
            users = Application().context.query(User).all()
        return users

    def __conver_user(self, user):
        team_dict = user.team
        if isinstance(user.team, Team):
            team_dict = user.team.__dict__
        user_dict = user.__dict__
        user_dict["team"] = team_dict
        user_json = Pykson().from_json(user_dict, UserJson, accept_unknown=True)
        return Pykson().to_dict_or_list(user_json)

    def __is_login(self, user):
        try:
            users = Application().context.query(User).filter(User.login == user.login).first()
        except AttributeError:
            Application().context.rollback()
            users = Application().context.query(User).filter(User.login == user.login).first()
        if users:
            return True
        return False

    def __get_filter_user(self, id_user):
        try:
            user = Application().context.query(User).filter(User.id == id_user)
        except AttributeError:
            Application().context.rollback()
            user = Application().context.query(User).filter(User.id == id_user)
        return user

