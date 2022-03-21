import subprocess
from time import time
from sys import getsizeof


class StartFileProgram:
    def __init__(self, path_file, time_out):
        self.__path_file = str(path_file).replace("\\", "/")
        self.__process = None
        self.__time_out = time_out

    @property
    def process(self):
        return self.__process

    def create_sub_proces(self):
        self.__process = subprocess.Popen([self.__path_file], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)

    def start_process(self, input_process):
        try:
            start_time = time()
            outs, errs = self.__process.communicate(input=input_process, timeout=self.__time_out * 1000)
            end_time = time() - start_time
            sizeof = getsizeof(self.__process)
            outs = str(outs.decode())
            errs = str(errs.decode())
            return [outs, errs, end_time * 1000, sizeof]
        except TimeoutError:
            self.__process.kill()
            return [None, 4, 0, 0]