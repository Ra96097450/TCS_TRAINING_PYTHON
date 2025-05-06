from multiprocessing import Pool
import time

def square(x):
    time.sleep(1)  # Simulate a time-consuming task
    return x * x

if __name__ == "__main__":
    with Pool(4) as p:  # Create a pool of 4 processes
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        results = p.map(square, numbers)

    print(results)
