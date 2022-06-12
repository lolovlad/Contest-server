from pykson import JsonObject, IntegerField, StringField, BooleanField


class TeamToUser(JsonObject):

    id = IntegerField()
    id_contest = IntegerField(default_value=0)
    name_team = StringField(default_value="")
    is_solo = BooleanField(default_value=False)
    state_contest = IntegerField(default_value=0)