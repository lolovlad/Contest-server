from enum import Enum


class Rating(Enum):
    OK = 1
    COMPILATION_ERROR = 2
    WRONG_ANSWER = 3
    PRESENTATION_ERROR = 4
    TIME_LIMIT_EXCEEDED = 5
    MEMORY_LIMIT_EXCEEDED = 6
    OUTPUT_LIMIT_EXCEEDED = 7
    RUN_TIME_ERROR = 8
    PRECOMPILE_CHECK_FAILED = 9
    IDLENESS_LIMIT_EXCEEDED = 10


class Grading:
    def __init__(self, size_memory):
        self.__size_memory = size_memory

    def grading(self, correct_answer, code_error, time, size_memory):
        if code_error == 1:
            return Rating.RUN_TIME_ERROR
        elif code_error == 2:
            return Rating.PRESENTATION_ERROR
        elif code_error == 3:
            return Rating.OUTPUT_LIMIT_EXCEEDED
        elif code_error == 4:
            return Rating.TIME_LIMIT_EXCEEDED
        elif size_memory > self.__size_memory:
            return Rating.MEMORY_LIMIT_EXCEEDED
        elif correct_answer:
            return Rating.OK
        elif correct_answer is False:
            return Rating.WRONG_ANSWER




