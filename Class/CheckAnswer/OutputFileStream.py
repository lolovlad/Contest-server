class OutputFileStream:
    def __init__(self, path_dir):
        self.__path_dir = path_dir

    def read_output(self, output_data):
        try:
            with open(self.__path_dir, "r") as file:
                output = file.readlines()
            return list(map(lambda x: x[:-2], output))
        except FileNotFoundError:
            return "FileNotFound"
