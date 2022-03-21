from pykson import JsonObject, IntegerField, ListField


class SubTest(JsonObject):
    score = IntegerField()
    filling_type_variable = ListField(str)
    answer = ListField(str)
