from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.User import User
from pykson import Pykson


class Users(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument("type", type=int)
    user_parser.add_argument("name", type=str)
    user_parser.add_argument("sename", type=str)
    user_parser.add_argument("login", type=str)
    user_parser.add_argument("password", type=str)

    def put(self, id_user):
        args = self.user_parser.parse_args()
        now_user = Application().context.query(User).filter(User.id == id_user).first()
        now_user.login = args.login
        now_user.name = args.name
        now_user.sename = args.sename
        now_user.type = args.type
        if len(args.password) > 0:
            now_user.password = args.password
        Application().context.commit()
        return {"data": "ok"}

    def delete(self, id_user):
        Application().context.query(User).filter(User.id == id_user).delete()
        return {"data": "ok"}