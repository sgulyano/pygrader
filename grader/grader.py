import os
import sys
import resource
import subprocess
import signal
import argparse

def setlimits():
    # Set maximum CPU time to 1 second in child process, after fork() but before exec()
    #os.setsid()
    print("Setting resource limit in child (pid %d)" % os.getpid())
    resource.setrlimit(resource.RLIMIT_CPU, (10, 20))

def main():
    print("CPU limit of parent (pid %d)" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU))
    p = subprocess.Popen(["python", "stone_pile.py"], preexec_fn=setlimits, stdin=open('1.in'), stderr=subprocess.STDOUT)
    print("CPU limit of parent (pid %d) after startup of child" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU))
    print(p.wait())
    print("CPU limit of parent (pid %d) after child finished executing" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU))
    print(p)

if __name__ == '__main__':
    #python grader.py -s problems/stone_pile/stone_pile.py -i problems/stone_pile/input -o problems/stone_pile/output -cpu 2 -mem 32
    parser = argparse.ArgumentParser()
    parser.add_argument('-s' 		,'--src'			,type=str   , required=True	    ,help='Path to source code')
    parser.add_argument('-i' 		,'--input'			,type=str   , required=True	    ,help='Input directory')
    parser.add_argument('-o'		,'--output'         ,type=str   , required=True	    ,help='Output directory (or ground truth)')
    parser.add_argument('-t'		,'--temp'		    ,type=str   , default='./'		,help='Temporary directory for storing user output (default = ./)')
    parser.add_argument('-cpu'		,'--cpu-time-limit'	,type=int   , default=1	        ,help='CPU Time limit (default = 1)')
    parser.add_argument('-mem'		,'--memory-limit'	,type=int   , default=16		,help='Memory limit in MB (default = 16MB)')
    args = parser.parse_args()
    print(args)

    assert(os.path.isfile(args.src))
    assert(os.path.isdir(args.input))
    assert(os.path.isdir(args.output))
    assert(os.path.isdir(args.temp))
    assert(isinstance(args.cpu_time_limit, int))
    assert(isinstance(args.memory_limit, int))

    file_list = []
    num_test = 0
    while True:
        input_file = os.path.join(args.input, f"{num_test+1}.in")
        output_file = os.path.join(args.output, f"{num_test+1}.out")
        num_test += 1
        if not os.path.isfile(input_file) or not os.path.isfile(output_file):
            break
        file_list.append((input_file, output_file))
    print(file_list)
    
#os.killpg(os.getpgid(p.pid), signal.SIGTERM)  # Send the signal to all the process groups
##!/usr/bin/env python3
## -*- coding: utf-8 -*-
#"""
#Created on Fri Nov 22 13:54:50 2019
#
#@author: yoyo
#"""
#
#import os
#import sys
#import resource
#import subprocess
#
#def setlimits():
#    # Set maximum CPU time to 1 second in child process, after fork() but before exec()
#    print "Setting resource limit in child (pid %d)" % os.getpid()
#    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
#
#print "CPU limit of parent (pid %d)" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU)
#p = subprocess.Popen(['python', 'stone_pile.py'], preexec_fn=setlimits)
#print "CPU limit of parent (pid %d) after startup of child" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU)
#p.wait()
#print "CPU limit of parent (pid %d) after child finished executing" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU)
#
### importing libraries 
##import signal 
##import resource 
##import subprocess
##import os 
##import sys
##
### checking time limit exceed 
##def time_exceeded(signo, frame): 
##    print("Time's up !", signo, frame) 
##    raise SystemExit(1)     
##
##def set_max_runtime(seconds=1): 
##    # setting up the resource limit 
##    soft, hard = resource.getrlimit(resource.RLIMIT_CPU) 
##    resource.setrlimit(resource.RLIMIT_CPU, (seconds, seconds)) 
##    signal.signal(signal.SIGXCPU, time_exceeded) 
##
##def time_limit(seconds:float):
##    def decorator(function):
##        def wrapper(*args, **kwargs):
##            set_max_runtime(seconds)
##            function(*args, **kwargs)
##        return wrapper
##    return decorator
##
### checking memory limit exceed 
##def set_max_memory(mem_in_b=1024):
##    resource.setrlimit(resource.RLIMIT_DATA, (mem_in_b, mem_in_b*2))
##
##def memory_limit(mem_in_b:int):
##    def decorator(function):
##        def wrapper(*args, **kwargs):
##            set_max_memory(mem_in_b)
##            try:
##                function(*args, **kwargs)
##            except MemoryError:
##                sys.stderr.write('\n\nERROR: Memory Exception\n')
##                sys.exit(1)
##        return wrapper
##    return decorator
##
##
##def setlimits():
##    set_max_runtime(1.5)
##
###@memory_limit(mem_in_b=1024*1024*1024)
###@time_limit(seconds=1.5)
##def main():
###    myinput = open('1.in')
###    myoutput = open('1.out', 'w')
###    myerror = open('1.err', 'w')
###    
##    import subprocess
##    subprocess.Popen('ulimit -t 1; python stone_pile.py < 1.in', shell=True)
##
##    
###    p = subprocess.Popen(['python', 'stone_pile.py'], preexec_fn=setlimits, stdin=myinput, stdout = myoutput)
###    print(p)
###    output, err = p.communicate()
###    print(output)
###    print(err)
###    p.wait()
###    a = []
###    while True: 
###        a.append(2)
###        print(resource.getrusage(resource.RUSAGE_SELF))
###                
###    print('My memory is limited to 80%.')
##    
### max run time of 15 millisecond 
##if __name__ == '__main__': 
##    main()
##
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
