import time

with open('file2.txt', 'w') as file:
    for i in range(5):
        time.sleep(1)
        file.write(str(i) + '\n')
    file.write('wow')
