#!/usr/bin/env python3.7.7
# -*- Coding: UTF-8 -*-

import time
from multiprocessing import Pool
from itertools import repeat
from helpers.timer import Timer
t = Timer()

def f_loop(a_list, b_list):
    '''Soma quadrática com loop'''
    out = 0
    for n in a_list:
        #print(b_list, '---', n)
        out += n*n
        #time.sleep(0.1)
    #time.sleep(0.5)
    return out

def f_single(b_list, n):
    '''Soma quadrática sem loop'''
    #print(b_list, '---', n)
    result = n*n
    #print(result)
    #time.sleep(0.5)
    return result

def f_amp(a_list, b_list):
    '''Paralelização'''
    pool = Pool(processes=5)
    result = pool.starmap(f_single, zip(repeat(b_list), a_list))
    pool.close()
    pool.join()
    #time.sleep(0.5)
    print(result)
    return sum(result)

###################################################################

# Definir lista com índices - valores de n
a_list = list(range(0,20))
# Definir lista com outros argumentos
b_list = [[23,24,37,255], 11, 22, 'string']

t.start()
print('Single loop')
print(f_loop(a_list, b_list))
t.stop()

t.start()
print('Multiprocess loop')
print(f_amp(a_list, b_list))
t.stop()
