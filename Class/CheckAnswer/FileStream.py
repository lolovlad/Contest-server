from Class.PathFileDir import PathFileDir
from subprocess import Popen


class FileStream:
    def __init__(self, name_dir):
        self.__file = None
        self.__name_dir = name_dir

    def __create_file(self):
        name_file = PathFileDir.abs_path(f"Answers/{self.__name_dir}/input.txt")
        PathFileDir.create_dirs(name_file)
        self.__file = name_file

    def start_stream(self, input_data):
        self.__create_file()
        PathFileDir.write_file(self.__file, "\n".join(input_data))
        return None

    def close_stream(self):
        path = str(self.__file)[:-10]
        PathFileDir.delete_dir(PathFileDir.str_to_abs_path(path))