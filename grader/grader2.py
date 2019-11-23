#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:24:54 2019

@author: yoyo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 13:54:50 2019

@author: yoyo
"""

# importing libraries 
import signal 
import resource 
import subprocess
import os 
import sys

# checking time limit exceed 
def time_exceeded(signo, frame): 
    print("Time's up !", signo, frame) 
    raise SystemExit(1)     

def set_max_runtime(seconds=1): 
    # setting up the resource limit 
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU) 
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard)) 
    signal.signal(signal.SIGXCPU, time_exceeded) 

def time_limit(seconds:float):
    def decorator(function):
        def wrapper(*args, **kwargs):
            set_max_runtime(seconds)
            function(*args, **kwargs)
        return wrapper
    return decorator

# checking memory limit exceed 
def set_max_memory(mem_in_b=1024):
    resource.setrlimit(resource.RLIMIT_DATA, (mem_in_b, mem_in_b*2))

def memory_limit(mem_in_b:int):
    def decorator(function):
        def wrapper(*args, **kwargs):
            set_max_memory(mem_in_b)
            try:
                function(*args, **kwargs)
            except MemoryError:
                sys.stderr.write('\n\nERROR: Memory Exception\n')
                sys.exit(1)
        return wrapper
    return decorator

#@memory_limit(mem_in_b=1024*1024)
@time_limit(seconds=1)
def main():
    os.system('python stone_pile.py < 1.in')
    #a = []
    #while True: 
    #    a.append(2)
    #    #print(resource.getrusage(resource.RUSAGE_SELF))
    #            
    print('My memory is limited to 80%.')
    
# max run time of 15 millisecond 
if __name__ == '__main__': 
    main()

##
##
###import os
###import sys
###import resource
###import subprocess
###
###def setlimits():
###    # Set maximum CPU time to 1 second in child process, after fork() but before exec()
###    print "Setting resource limit in child (pid %d)" % os.getpid()
###    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
###
###print "CPU limit of parent (pid %d)" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU)
###p = subprocess.Popen(["./child.py"], preexec_fn=setlimits)
###print "CPU limit of parent (pid %d) after startup of child" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU)
###p.wait()
###print "CPU limit of parent (pid %d) after child finished executing" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU)
##
##
##
##
###
###def memory_limit():
###    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
###    resource.setrlimit(resource.RLIMIT_AS, (64*1024*1024, hard))
###
###def get_memory():
###    with open('/proc/meminfo', 'r') as mem:
###        free_memory = 0
###        for i in mem:
###            sline = i.split()
###            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
###                free_memory += int(sline[1])
###    return free_memory
###
###def main():
###    a = [[] for i in range(100000)]
###    return 1+2
###
###if __name__ == '__main__':
###    memory_limit() # Limitates maximun memory usage to half
###    try:
###        main()
###    except MemoryError:
###        sys.stderr.write('\n\nERROR: Memory Exception\n')
###        sys.exit(1)
