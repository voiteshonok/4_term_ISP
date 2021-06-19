from posixpath import dirname
from time import time, sleep
import os, stat
from shutil import copyfile, rmtree
import json

import docker
from docker.types import Mount

from .custom_types import Verdict


class Checker:
    path_to_dockerfile = 'blog/doc/Dockerfile'
    path_to_usage = 'blog/doc/usage.py'

    def __init__(self, task, code) -> None:
        self.task = task
        self.code = code

    
    def __make_files(self):
        dir_name = str(int(time()*1000))
        tempo = os.path.join('../media_cdn', dir_name)
        os.mkdir(tempo)
        copyfile(self.task.input.path, os.path.join(tempo, 'input.txt'))
        copyfile(self.task.output.path, os.path.join(tempo, 'expected_output.txt'))
        with open(os.path.join(tempo, 'submission.py'), 'w') as file:
            file.write(self.code)
        copyfile(self.path_to_dockerfile, os.path.join(tempo, 'Dockerfile'))
        copyfile(self.path_to_usage, os.path.join(tempo, 'usage.py'))
        with open(os.path.join(tempo, "params.json"), "w") as file:
            json.dump({"time": self.task.time_limit, "memory": self.task.memory_limit}, file)
        
        return dir_name, tempo

    def __run_docker(self, dir_name, tempo):
        client = docker.from_env()

        image, logs = client.images.build(path='.', dockerfile=os.path.join(tempo, 'Dockerfile'), tag=int(round(time()*1000)), rm=True)

        client.containers.run(image.attrs['Id'], detach=False,
                                        volumes={f'/home/slava/tester/{dir_name}/': {"bind": f"/usr/src/app/", "mode": "rw"}
                                                },
                                       network_disabled=True,)
                                       
        client.containers.prune()
        try:
            client.images.remove(image.attrs['Id'], force=True)
        except:
            pass

    def __check_outputs(self, dirname, tempo):
        try:
            with open(os.path.join(tempo, 'output.txt'), 'r') as output:
                with open(os.path.join(tempo, 'expected_output.txt'), 'r') as expected_output:
                    if output.read() == expected_output.read():
                        return Verdict.OK
                    else:
                        return Verdict.WA
        except:
            return Verdict.RE

    def __run_submision(self, dir_name, tempo):
        self.__run_docker(dir_name, tempo)
    
        try:
            with open(os.path.join(tempo, 'status.json'), "r") as file:
                try:
                    status = json.load(file)['status']
                except:
                    return Verdict.ML
        except:

            return Verdict.RE
        
        
        if status != Verdict.OK.name:
            return Verdict(status)
    
        status = self.__check_outputs(dir_name, tempo)

        return status


    def run_submission(self):
        dir_name, tempo = self.__make_files()
        
        status = self.__run_submision(dir_name, tempo)
        rmtree(tempo, ignore_errors=True)

        return status

