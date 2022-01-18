from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.User import User


class Login(Resource):
    login_parser = reqparse.RequestParser()
    login_parser.add_argument("login", type=str)
    login_parser.add_argument("password", type=str)

    def post(self):
        args = self.login_parser.parse_args()
        user = Application().context.query(User).filter(User.login == args["login"]).first()
        if user and user.check_password(args["password"]):
            user_data = {"name": user.name,
                         "sename": user.sename,
                         "type": user.type}
            return user_data
        else:
            return {"error": "неправильный логин или пароль"}