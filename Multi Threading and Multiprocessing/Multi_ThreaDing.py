import threading

def cube(num):
   print("Cube: {}" .format(num * num*num))

def squre(n):
    print('The squre of the given number is: {} '.format(n*n))

if __name__=="__main__":

    t1=threading.Thread(target=cube, args=(10,))
    t2=threading.Thread(target=squre,args=(10,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Done!")