import json
from pathlib import Path
from pykson import Pykson


class JsonFileParser:
    def __init__(self, configuration_file_name):
        self.__name_dir = "Files"
        dir_path = Path(Path(__file__).parent).parent
        self.__path = Path(dir_path,  self.__name_dir, configuration_file_name)
        self.__config = {}

    def load(self, model):
        with open(self.__path, "r") as read_file:
            self.__config = json.load(read_file)
            deserializer_model = Pykson().from_json(self.__config, model)
            return deserializer_model

    def save(self):
        with open(self.__path, 'w') as outfile:
            json.dump(self.__config, outfile)