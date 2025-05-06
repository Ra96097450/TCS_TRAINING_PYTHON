import threading
import os

def task1():
    print("The name of the task1 thread:{}".format(threading.current_thread().name))
    print("The ID of the Process task1:{}".format(os.getpid()))


def task2():
    print("The name of the task2 thread:{}".format(threading.current_thread().name))
    print("The ID of the Process task2:{}".format(os.getpid()))


if __name__=="__main__":

    print("The ID of the process runing the main program:{}".format(os.getpid()))
    print("The Name of main Thread:{}",format(threading.current_thread().name))

    t1=threading.Thread(target=task1,name='func1')
    t2=threading.Thread(target=task2,name='func2')

    t1.start()
    t2.start()

    t1.join()
    t2.join()
