# import the time module 
import time

def countdown(t):
    for i in range(t-1,-1,-1):
        time.sleep(1)
        print(i)

t = int(input("Enter the time in seconds: "))
countdown(t)