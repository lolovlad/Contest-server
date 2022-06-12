from pykson import IntegerField, ObjectField, StringField, JsonObject


class TaskDB(JsonObject):
    id = IntegerField()
    id_contest = IntegerField()
    time_work = IntegerField()
    size_raw = IntegerField()
    type_input = IntegerField()
    type_output = IntegerField()
    name_test = StringField()
    description = StringField()
    description_input = StringField()
    description_output = StringField()

    path_test_file = StringField()

    type_task = IntegerField()
    number_shipments = IntegerField()