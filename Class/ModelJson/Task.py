from pykson import JsonObject, ObjectListField
from Class.ModelJson.Test import Test


class Task(JsonObject):
    setting_tests = ObjectListField(Test)