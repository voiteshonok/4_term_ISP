import docker
from docker.types import Mount

#from time import time
# import time

# client = docker.from_env()

# mount = Mount(target='/usr/src/app/', source='/home/slava/Desktop/doc', type='bind')


# image, logs = client.images.build(path='.', dockerfile='Dockerfile', tag=int(round(time.time()*1000)), rm=True)

# client.containers.run(image.attrs['Id'], detach=True, mounts=[mount])
# print(image.attrs['Id'])
# time.sleep(6)

# prune = client.images.remove(image.attrs['Id'], force=True)

# print(prune)
from enum import Enum
class Verdict(Enum):
    ML = "ML"
    TL = "TL"
    WA = "WA"
    OK = "OK"
    RE = "RE"

print(Verdict.ML.name)

