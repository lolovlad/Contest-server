from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.User import User


class Registration(Resource):
    registration_parser = reqparse.RequestParser()
    registration_parser.add_argument("login", type=str)
    registration_parser.add_argument("password", type=str)
    registration_parser.add_argument("name", type=str)
    registration_parser.add_argument("sename", type=str)
    registration_parser.add_argument("type", type=int)

    def post(self):
        args = self.registration_parser.parse_args()
        if Application().context.query(User).filter(User.login == args["login"]).first():
            return {"error": "такой логин же существует"}
        user = User(name=args["name"],
                    sename=args["sename"],
                    login=args["login"],
                    type=args["type"])
        user.password = args["password"]
        Application().context.add(user)
        Application().context.commit()
        return {"data": "ok"}
