import threading
import math


def worker():
    """thread worker function"""
    print(math.sin(25))
    print('Worker')
    mt


threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append
    t.start()