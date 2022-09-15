from contextlib import redirect_stderr
import time
import asyncio
from threading import Thread

a = ""
i = 0
c = 0

t1 = int(time.time())

def compteur(a,t1):
    while True:
        t2 = int(time.time())
        c = t2 - t1  
        if c == 26:
            t1 = t2
            print("action done")
            time.sleep (0.5)  
        if c <= 10:
            a = "red"

        elif c > 10 and c <= 15:
            a = "orange"

        elif c > 15 and c <= 25:
            a = 'green'
        print(a)  



# create two new threads
th1 = Thread(target=compteur(a,t1))

# start the threads
th1.start()

# wait for the threads to complete
th1.join()





