from Class.PathFileDir import PathFileDir
from subprocess import Popen


class InputStream:
    def __init__(self, name_dir):
        self.__file = None
        self.__name_dir = name_dir
        self.__create_file()

    def __create_file(self):
        name_file = PathFileDir.abs_path(f"Answers/{self.__name_dir}")
        PathFileDir.create_dirs(name_file)
        self.__file = name_file

    def start_stream(self, input_data):
        return "\n".join(input_data).encode()

    def close_stream(self):
        PathFileDir.delete_dir(self.__file)