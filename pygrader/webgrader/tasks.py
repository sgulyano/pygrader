import os
from celery import shared_task
from django.conf import settings

from .models import Submission

import grader


@shared_task
def grading(sub_pk):
    print(grader.run_all_tests)
    
    sub = Submission.objects.get(pk=sub_pk)
    src = os.path.join(settings.MEDIA_ROOT, sub.src_code.path)
    testcase_folder, _ = os.path.splitext(sub.problem.testcases.path)

    args = {'src': src, 
            'input': os.path.join(testcase_folder, 'input'), 
            'output': os.path.join(testcase_folder, 'output'), 
            'cpu_time_limit': sub.problem.cpu_limit, 
            'memory_limit': sub.problem.mem_limit}
    
    sub.result = grader.run_all_tests(args)
    sub.score = grader.get_score(sub.result, 100)  # change field
    sub.save() # this will update only
    return sub_pk