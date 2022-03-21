class OutputStream:
    def __init__(self, path_dir):
        self.__path_dir = path_dir

    def read_output(self, output_data):
        output_data = output_data.split("\r\n")
        return output_data[:-1]

