#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:57:00 2019

@author: yoyo
"""

import itertools
import numpy as np
import resource
import os
import random
#print("CPU limit of child (pid %d)" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU))

n = int(input())
num = input()
arr = np.array([int(i) for i in num.split()])
s = arr.sum()
b = []
for i in range(1000000):
    b.append(random.sample(range(10, 1000000000), 100000000))
best = np.inf
for i in itertools.product([True, False], repeat=n):
    val = abs(s - 2*arr[list(i)].sum())
    if best > val:
        best = val
print(best)
