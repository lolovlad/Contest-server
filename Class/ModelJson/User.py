from pykson import IntegerField, ObjectField, StringField, JsonObject
from Class.ModelJson.TeamToUser import TeamToUser


class User(JsonObject):
    id = IntegerField()
    login = StringField()
    name = StringField()
    sename = StringField()
    secondname = StringField()
    type = IntegerField()
    team = ObjectField(TeamToUser)