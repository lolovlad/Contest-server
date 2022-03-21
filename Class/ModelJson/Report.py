from pykson import JsonObject, StringField, ObjectField, ObjectListField
from Class.ModelJson.TestReport import TestReport


class Report(JsonObject):
    list_report = ObjectListField(TestReport)