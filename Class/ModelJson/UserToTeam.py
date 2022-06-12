from pykson import JsonObject, IntegerField, StringField


class UserToTeam(JsonObject):

    id = IntegerField()
    login = StringField()
    name = StringField()
    sename = StringField()
    secondname = StringField()
    password = StringField()

    type = IntegerField()