import os
import sys
import resource
import subprocess
import signal
import random
import argparse

import difflib
import tempfile

RUN_COMPLETE = 0
TIME_LIMIT = -24
MEM_LIMIT = 3


def testing(src, inp, out, cpu, mem):
    """
    Check if src gives correct output
        0 = incorrect answer
        1 = correct answer
        2 = time limit exceeds
        3 = memory limit exceeds
        otherwise compile error
    """
    def setlimits():
        # Set maximum CPU time to 1 second in child process, after fork() but before exec()
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu*2))
    
    temp = tempfile.NamedTemporaryFile(mode="wb")
    # tmp_file = tmp + ''.join([str(random.randint(0, 9)) for i in range(10)])

    p = subprocess.Popen(["python", src], preexec_fn=setlimits, stdin=open(inp), stdout=temp, stderr=subprocess.STDOUT)
    
    res = p.wait()
    
    if res == RUN_COMPLETE:
        result = subprocess.run(['diff', '-BEZb', temp.name, out], stdout=subprocess.PIPE)
        if not result.stdout:
            status = 1
        else:
            status = 0
    elif res == TIME_LIMIT:
        status = 2
    elif res == MEM_LIMIT:
        status = 3
    else:
        result = subprocess.run(['less', temp.name], stdout=subprocess.PIPE)
        print(result.stdout.decode())
        status = 4
    temp.close()
    return status

def run_all_tests(args):
    # get list of tests
    file_list = []
    num_test = 0
    while True:
        input_file = os.path.join(args['input'], f"{num_test+1}.in")
        output_file = os.path.join(args['output'], f"{num_test+1}.out")
        num_test += 1
        if not os.path.isfile(input_file) or not os.path.isfile(output_file):
            break
        file_list.append((input_file, output_file))
    
    # run user program on each test
    all_results = ''
    print("\tTesting set: %s" % os.path.dirname(file_list[0][0]))
    print('\tRunning %s, \t [CPU=%ds, MEM=%dMB]' % (args['src'], args['cpu_time_limit'], args['memory_limit']) )
    for inp, out in file_list:
        results = testing(args['src'], inp, out, args['cpu_time_limit'], args['memory_limit'])
        if results == 1:
            print("\t\t%s \tcorrect" % os.path.basename(inp))
            all_results += 'C'
        elif results == 0:
            print("\t\t%s \twrong" % os.path.basename(inp))
            all_results += 'X'
        elif results == 2:
            print("\t\t%s \ttime limit exceeds" % os.path.basename(inp))
            all_results += 'T'
        elif results == 3:
            print("\t\t%s \tmemory limit exceeds" % os.path.basename(inp))
            all_results += 'M'
        else:
            print("\t\t%s \tcompiler error" % os.path.basename(inp))
            all_results += 'E'
    return all_results

def get_score(result, max_score):
    ratio = sum([x == 'C' for x in result]) / float(len(result))
    return int(max_score * ratio)


if __name__ == '__main__':
    #python grader.py -s problems/stone_pile/stone_pile.py -i problems/stone_pile/input -o problems/stone_pile/output -cpu 2 -mem 32
    parser = argparse.ArgumentParser()
    parser.add_argument('-s' 		,'--src'			,type=str   , required=True	    ,help='Path to source code')
    parser.add_argument('-i' 		,'--input'			,type=str   , required=True	    ,help='Input directory')
    parser.add_argument('-o'		,'--output'         ,type=str   , required=True	    ,help='Output directory (or ground truth)')
    parser.add_argument('-cpu'		,'--cpu-time-limit'	,type=int   , default=1	        ,help='CPU Time limit (default = 1)')
    parser.add_argument('-mem'		,'--memory-limit'	,type=int   , default=16		,help='Memory limit in MB (default = 16MB)')
    args = parser.parse_args()

    assert(os.path.isfile(args.src))
    assert(os.path.isdir(args.input))
    assert(os.path.isdir(args.output))
    assert(isinstance(args.cpu_time_limit, int))
    assert(isinstance(args.memory_limit, int))
    
    args = vars(args)
    
    all_results = run_all_tests(args)
    print(all_results)

    print(get_score(all_results, 100))