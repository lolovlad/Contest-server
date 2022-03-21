from Class.CheckAnswer.OutputStream import OutputStream
from Class.CheckAnswer.OutputFileStream import OutputFileStream
from Class.PathFileDir import PathFileDir


class OutputData:
    def __init__(self, path):
        self.__output_stream = OutputStream(path)
        self.__output_file_stream = OutputFileStream(path)

    def creating_output_data(self, type_data):
        if type_data == 1:
            return self.__output_stream
        elif type_data == 2:
            return self.__output_file_stream