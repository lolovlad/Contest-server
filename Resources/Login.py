from flask_restful import Resource, reqparse
from Class.StartAplication import Application

from Model.User import User
from Model.Team import Team

from Class.ModelJson.User import User as UserJson
from pykson import Pykson


class Login(Resource):
    login_parser = reqparse.RequestParser()
    login_parser.add_argument("login", type=str)
    login_parser.add_argument("password", type=str)

    def post(self):
        args = self.login_parser.parse_args()
        user = self.__get_user(args)
        if user is not None:
            if user.check_password(args.password):
                team_dict = {"id": 0}
                if user.team is not None:
                    team_dict = user.team.__dict__
                user_dict = user.__dict__
                user_dict["team"] = team_dict
                user_json = Pykson().from_json(user_dict, UserJson, accept_unknown=True)
                return {"message": "login", "data": {"user": Pykson().to_dict_or_list(user_json)}}
            else:
                return {"message": "error", "data": "неправильный логин или пароль"}
        else:
            return {"message": "error", "data": "неправильный логин или пароль"}

    def __get_user(self, args):
        try:
            user = Application().context.query(User).filter(User.login == args.login).first()
        except Exception:
            Application().context.rollback()
            user = Application().context.query(User).filter(User.login == args.login).first()
        return user
