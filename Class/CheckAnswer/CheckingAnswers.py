import threading
from os import chdir, getcwd
from json import dump, loads
from pykson import Pykson
from memory_profiler import memory_usage

from Class.JsonReadFile import JsonFileParser
from Model.Task import Task
from Class.StartAplication import Application

from Class.ModelJson.Task import Task as TaskJson
from Class.ModelJson.Report import Report
from Class.CheckAnswer.InputData import InputData
from Class.CheckAnswer.StartFileProgram import StartFileProgram
from Class.CheckAnswer.OutputData import OutputData
from Class.CheckAnswer.Grading import Grading

from Class.ModelJson.TestReport import TestReport
from Class.PathFileDir import PathFileDir


class CreateAnswers:
    def __init__(self):
        self.__pool_answer = []
        self.__len_thread = 5

    def pool_new_answer(self, answer):
        thread_answer = threading.Thread(target=check_answer, args=(answer,))
        thread_answer.start()


class CheckingAnswer:
    def __init__(self, test, type_input, type_output, timeout, size, file_answer):
        self.__test = test
        self.__type_input = type_input
        self.__type_output = type_output
        self.__timeout = timeout
        self.__file_answer = PathFileDir.str_to_abs_path(file_answer)
        self.__queue = []
        self.__create_queue()
        self.__report = Report()
        self.__grading = Grading(size)
        self.__GRADING = ["OK", "CE", "WA", "PE", "TL", "ML", "OL", "RE", "PCF", "IL"]

    def __create_queue(self):
        checkpoint_test = list(filter(lambda x: x.type_test == "test", self.__test.setting_tests))
        main_test = list(filter(lambda x: x.type_test == "main", self.__test.setting_tests))
        self.__queue.insert(0, checkpoint_test[0])
        main_test = list(sorted(main_test, key=lambda x: len(x.settings_test.necessary_test) and sum(x.settings_test.necessary_test)))
        self.__queue += main_test

    def start_examination(self):
        name_test = 1

        input_data = InputData()
        input_stream = input_data.creating_input_data(self.__type_input)

        work_dir = getcwd()

        file = PathFileDir.name_file_to_dir(self.__file_answer)
        path_file_program = PathFileDir.abs_path(f"Answers/{input_data.name_dir}/{file}")
        PathFileDir.move_file(self.__file_answer, path_file_program)
        chdir(PathFileDir.abs_path(f"Answers/{input_data.name_dir}"))

        output_data = OutputData(f"Answers/{input_data.name_dir}/output.txt")
        output_stream = output_data.creating_output_data(self.__type_output)

        program_file = StartFileProgram(path_file_program, self.__timeout)

        test_report = [TestReport() for _ in range(len(self.__queue))]

        for i, test in enumerate(self.__queue):
            start_checking = []
            test_report[i].point_sum = 0
            test_report[i].time = 0
            if len(test.settings_test.necessary_test) > 0:
                for necessary_test in test.settings_test.necessary_test:
                    start_checking.append(test_report[necessary_test - 1].state_report)
            else:
                start_checking.append(True)

            if all(start_checking) is False:
                test_report[i].state_report = False
                test_report[i].name_test = f"skip test"
                test_report[i].time = 0
                test_report[i].number_test = name_test
                test_report[i].memory = 0
                continue

            test_report[i].state_report = True
            for id_info_test, info_test in enumerate(test.tests):

                input_data = input_stream.start_stream(info_test.filling_type_variable)
                memory = memory_usage((program_file.create_sub_proces, ()), max_iterations=1)
                information = program_file.start_process(input_data)

                output_information = output_stream.read_output(information[0])

                if output_information == "FileNotFound":
                    information[1] = 2

                grading = self.__grading.grading(output_information == info_test.answer, information[1],
                                                 information[2], information[3])

                test_report[i].list_test_report.append(self.__GRADING[grading.value - 1])

                name_test += 1

                if test.settings_test.check_type == 1:
                    if test_report[i].list_test_report[-1] != "OK":
                        test_report[i].state_report = False
                        test_report[i].name_test = f"test {name_test}"
                        test_report[i].time += 0
                        test_report[i].number_test = name_test
                        break
                    else:
                        test_report[i].point_sum += info_test.score
                        test_report[i].number_test = name_test
                        test_report[i].time += int(information[2])
                    test_report[i].memory = int(sum(memory) / len(memory))

            if test_report[i].state_report:
                test_report[i].name_test = "test sucesfull"
                test_report[i].number_test = name_test

        chdir(work_dir)
        input_stream.close_stream()

        return test_report


def check_answer(answer):
    task = Application().context.query(Task).filter(Task.id == answer.id_task).first()
    path_file_test = task.path_test_file

    dir_path_file = PathFileDir.path_file(answer.path_programme_file)

    type_input = task.type_input
    type_output = task.type_output
    timeout = task.time_work
    size = task.size_raw
    test = JsonFileParser(path_file_test).load(TaskJson)
    checking_answer = CheckingAnswer(test, type_input, type_output, timeout, size, answer.path_programme_file)
    answer_json = checking_answer.start_examination()

    reports = Report()
    reports.list_report = answer_json

    path_file_report = f"{dir_path_file}/{PathFileDir.create_file_name('json')}"

    with open(path_file_report, 'w') as outfile:
        dump(loads(Pykson().to_json(reports)), outfile)

    answer.path_report_file = str(PathFileDir.abs_path(path_file_report))

    points = 0
    times = 0
    memory = []
    answers = []

    for i in answer_json:

        points += i.point_sum
        answers += i.list_test_report
        times += i.time
        memory.append(i.memory)

    answer.total = "OK"

    for i in answers:
        if i != "OK":
            answer.total = i

    answer.memory_size = int(sum(memory) / len(memory))

    answer.points = points
    answer.number_test = answer_json[-1].number_test
    answer.time = f"{times} ms"

    Application().context.commit()

