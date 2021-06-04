import signal
import resource
import json
  

def time_exceeded(signo, frame):
    raise TimeoutError()
  
def set_max_runtime(seconds):
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
    signal.signal(signal.SIGXCPU, time_exceeded)

def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))
  

if __name__ == '__main__':

    with open("params.json", "r") as file:
        params = json.load(file)

    print(params)
    set_max_runtime(params['time'] * 1.5)
    limit_memory(params["memory"])

    try:
        from submission import *
        sol()
    except TimeoutError:
        with open('status.json', "w") as file:
            json.dump({"status": "TL"}, file)
    except MemoryError:
        with open('status.json', "w") as file:
            json.dump({"status": "ML"}, file)
    except:
        with open('status.json', "w") as file:
            json.dump({"status": "RE"}, file)
    else:
        with open('status.json', "w") as file:
            json.dump({"status": "OK"}, file)