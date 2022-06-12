from pykson import IntegerField, ObjectListField, StringField, JsonObject, DateTimeField
from Class.ModelJson.TaskDB import TaskDB

from datetime import datetime


class Contest(JsonObject):
    id = IntegerField()
    name_contest = StringField()
    datetime_registration = DateTimeField(default_value=datetime.now())
    datetime_start = DateTimeField()
    datetime_end = DateTimeField()
    type = IntegerField()
    state_contest = IntegerField()
    tasks = ObjectListField(TaskDB)