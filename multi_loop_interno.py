#!/usr/bin/env python3.7.7
# -*- Coding: UTF-8 -*-

import time
from multiprocessing import Pool
from helpers.timer import Timer
t = Timer()

def f(a_list):
    '''
    Quadratic sum with internal loop
    '''
    out = 0
    for n in a_list:
        out += n*n
        time.sleep(0.1)
    return out

def f_amp(a_list):
    '''
    Paralellization with list chucks
    '''
    chunks = [a_list[i::5] for i in range(5)]
    pool = Pool(processes=5)
    result = pool.map_async(f, chunks)
    while not result.ready():
        time.sleep(0.5)
    return sum(result.get())

# Define list loop
a_list = list(range(0,20))

t.start()
print('Regular loop')
print(f(a_list))
t.stop()

t.start()
print('Multiprocess loop - with chunks')
print(f_amp(a_list))
t.stop()
