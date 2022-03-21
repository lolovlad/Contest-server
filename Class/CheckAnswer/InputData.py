from Class.CheckAnswer.InputStream import InputStream
from Class.CheckAnswer.FileStream import FileStream
from Class.PathFileDir import PathFileDir


class InputData:
    def __init__(self):
        self.__name_dir = PathFileDir.create_folder()
        self.__file_data = FileStream(self.__name_dir)
        self.__input_data = InputStream(self.__name_dir)

    @property
    def name_dir(self):
        return self.__name_dir

    def creating_input_data(self, type_data):
        if type_data == 1:
            return self.__input_data
        elif type_data == 2:
            return self.__file_data
