import subprocess
from time import time
from sys import getsizeof
from memory_profiler import memory_usage


class StartFileProgram:
    def __init__(self, virtual, input_stream, output_stream, type_compilation, time_out):
        self.__path_file = virtual.path_file_answer
        self.__input_stream = input_stream
        self.__output_stream = output_stream
        self.__process = None
        self.__time_out = time_out
        self.__python_compil = "C:/Users/Vlad/AppData/Local/Programs/Python/Python37/python.exe" if type_compilation == "Python" else None

    @property
    def process(self):
        return self.__process

    def __create_sub_proces(self):
        self.__process = subprocess.Popen(f"{self.__python_compil} {self.__path_file}", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)

    def start_process(self, input_in_process):
        input_data = self.__input_stream.start_stream(input_in_process)
        memory = memory_usage((self.__create_sub_proces, ()), max_iterations=1)
        try:
            start_time = time()
            outs, errs = self.__process.communicate(input=input_data, timeout=self.__time_out * 1000)
            end_time = time() - start_time
            sizeof = getsizeof(self.__process)
            outs = self.__output_stream.read_output(str(outs.decode()))
            errs = str(errs.decode())
            return [outs, errs, end_time * 1000, sizeof, memory]
        except TimeoutError:
            self.__process.kill()
            return [None, 4, 0, 0, memory]