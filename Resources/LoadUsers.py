from flask_restful import Resource, reqparse
from Class.StartAplication import Application
from Model.User import User


class LoadUsers(Resource):
    def post(self):
        users = Application().context.query(User).all()
        response = {
            "users": []
        }
        for user in users:
            response["users"].append({"id": user.id, "login": user.login, "name": user.name, "sename": user.sename, "type": user.type})
        return response
