from pykson import IntegerField, ObjectListField, StringField, JsonObject, BooleanField, DateTimeField, ObjectField
from Class.ModelJson.UserToTeam import UserToTeam


class ContestTeam(JsonObject):
    id = IntegerField()
    name_contest = StringField()
    datetime_registration = DateTimeField()
    datetime_start = DateTimeField()
    datetime_end = DateTimeField()
    type = IntegerField()


class Team(JsonObject):
    id = IntegerField()
    id_contest = IntegerField()
    name_team = StringField()
    is_solo = BooleanField()
    state_contest = IntegerField()
    users = ObjectListField(UserToTeam)
    contest = ObjectField(ContestTeam)
