from pykson import JsonObject, StringField, ObjectField, ObjectListField
from Class.ModelJson.SubTest import SubTest
from Class.ModelJson.SettingsTest import SettingsTest


class Test(JsonObject):
    type_test = StringField()
    settings_test = ObjectField(SettingsTest)
    tests = ObjectListField(SubTest)
