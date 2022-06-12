from pykson import IntegerField, ObjectField, StringField, JsonObject, DateTimeField
from Class.ModelJson.TeamToUser import TeamToUser
from Class.ModelJson.UserToTeam import UserToTeam
from Class.ModelJson.TaskDB import TaskDB

from datetime import datetime


class Answer(JsonObject):
    date_send = DateTimeField()
    id = IntegerField()
    team = ObjectField(TeamToUser)
    user = ObjectField(UserToTeam)
    task = ObjectField(TaskDB)
    type_compiler = IntegerField()
    total = StringField()
    time = StringField()
    memory_size = IntegerField()
    number_test = IntegerField()
    points = IntegerField()

    path_report_file = StringField()
    path_programme_file = StringField()