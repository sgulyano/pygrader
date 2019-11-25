import os
from celery import shared_task
from django.conf import settings

from .models import Problem, Submission

import grader


@shared_task
def grading(sub_pk, pb_pk):
    print(grader.run_all_tests)
    
    sub = Submission.objects.get(pk=sub_pk)
    src = os.path.join(settings.MEDIA_ROOT, sub.src_code.path)

    pb = Problem.objects.get(pk=pb_pk)

    args = {'src': src, 
            'input': '/home/yoyo/Desktop/pygrader/grader/problems/stone_pile/input', 
            'output': '/home/yoyo/Desktop/pygrader/grader/problems/stone_pile/output', 
            'temp': './', 'cpu_time_limit': 2, 
            'memory_limit': 32}
    result = grader.run_all_tests(args)
    
    sub.score = grader.get_score(result, 100)  # change field
    sub.save() # this will update only
    return sub_pk