from pykson import JsonObject, ListField, IntegerField


class SettingsTest(JsonObject):
    limitation_variable = ListField(str)
    necessary_test = ListField(int)
    check_type = IntegerField()
