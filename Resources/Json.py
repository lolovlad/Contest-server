from flask_restful import Resource, reqparse
from Class.JsonView import JsonView
from json import loads


class Json(Resource):
    name_file_parser = reqparse.RequestParser()
    name_file_parser.add_argument("list_name_file", type=str)

    def get(self):
        args = self.name_file_parser.parse_args()
        name_file_parser = loads(args.list_name_file)

        response = {
            "message": "load_json_test_file",
            "data": {"jsons_view": {}}
        }
        for name_file in name_file_parser["name_files"]:
            file_json = name_file
            view = JsonView(file_json)
            view.generate_view()
            response["data"]["jsons_view"][name_file] = view.view
        return response
