from time import time, sleep
import os, stat
from shutil import copyfile, rmtree
from .task import Task
import json

import docker
from docker.types import Mount

from .custom_types import Verdict


class Checker:
    path_to_dockerfile = 'blog/doc/Dockerfile'
    path_to_usage = 'blog/doc/usage.py'

    def __init__(self, task, path_to_file) -> None:
        self.task = task
        self.path_to_file = path_to_file

    
    def __make_files(self):
        dir_name = str(int(time()*1000))
        os.mkdir(dir_name)
        copyfile(self.task.path_to_input, os.path.join(dir_name, 'input.txt'))
        copyfile(self.task.path_to_expected_output, os.path.join(dir_name, 'expected_output.txt'))
        copyfile(self.path_to_file, os.path.join(dir_name, 'submission.py'))
        copyfile(self.path_to_dockerfile, os.path.join(dir_name, 'Dockerfile'))
        copyfile(self.path_to_usage, os.path.join(dir_name, 'usage.py'))
        with open(os.path.join(dir_name, "params.json"), "w") as file:
            json.dump({"time": self.task.time_limit, "memory": self.task.memory_limit}, file)

        return dir_name

    def __run_docker(self, dir_name):
        client = docker.from_env()

        mount = Mount(target='/usr/src/app/', source=os.path.join(os.getcwd(), dir_name), type='bind')


        image, logs = client.images.build(path='.', dockerfile=os.path.join(dir_name, 'Dockerfile'), tag=int(round(time()*1000)), rm=True)

        client.containers.run(image.attrs['Id'], detach=True, mounts=[mount])
        
        sleep(self.task.time_limit * 2)

        client.images.remove(image.attrs['Id'], force=True)

    def __check_outputs(self, dirname):
        try:
            with open(os.path.join(dirname, 'output.txt'), 'r') as output:
                with open(os.path.join(dirname, 'expected_output.txt'), 'r') as expected_output:
                    if output.read() == expected_output.read():
                        return Verdict.OK
                    else:
                        return Verdict.WA
        except:
            return Verdict.RE


    def run_submission(self):
        dir_name = self.__make_files()
        
        self.__run_docker(dir_name)
    
        try:
            with open(os.path.join(dir_name, 'status.json'), "r") as file:
                try:
                    status = json.load(file)['status']
                except:
                    status = Verdict.ML
        except:
            return Verdict.RE
        
        
        if status != Verdict.OK.name:
            print(status)
            return status
    
        status = self.__check_outputs(dir_name)

        print(status)

        rmtree(dir_name, ignore_errors=True)

        return status

def test():
    task = Task(slug_name='test', path_to_input='blog/doc/data/input/echo.txt', path_to_expected_output='blog/doc/data/output/echo.txt', time_limit=1, memory_limit=250)

    ch = Checker(task, 'blog/doc/data/submissions/1.py')
    return ch.run_submission()

