

def sol():
    with open('input.txt', 'r') as input:
        with open('output.txt', 'w') as output:
            for line in input:
                output.write(line)
    a = []

    while True:
        a.append([0] * 255)
            