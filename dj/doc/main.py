import docker
from docker.types import Mount

from time import time

client = docker.from_env()

mount = Mount(target='/usr/src/app/', source='/home/slava/Desktop/doc', type='bind')

image, logs = client.images.build(path='.', dockerfile='Dockerfile', tag=int(round(time()*1000)))
image2, logs = client.images.build(path='.', dockerfile='Dockerfile2', tag=int(round(time()*1000)))

client.containers.run(image.attrs['Id'], detach=True, mounts=[mount])
client.containers.run(image2.attrs['Id'], detach=True, mounts=[mount])
