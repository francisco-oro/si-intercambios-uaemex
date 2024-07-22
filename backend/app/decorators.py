import time
import math

"""Decorator to measure the time taken by a function"""
def timer(func): #time(fib)
    
    def wrapper(*args, **kwargs):
        start = time.time()
        
        value = func(*args, **kwargs) #fib(3) 
        
        end = time.time()
    
        total_time = end - start
        
        print(f'Time taken: {total_time} seconds')
        return value
    
    return wrapper

@timer
def fact(num):
    time.sleep(2)
    return math.factorial(num)
    
print(fact(5)) 