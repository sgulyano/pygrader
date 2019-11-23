from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .models import Problem, Submission
from .forms import SubmissionForm

import grader

from django.db.models import Count, Min
from django.db.models import Q

@login_required
def index(request):
    #aa = Problem.objects.values('problem_title', 'submission__uploaded_at').annotate(c = Count('submission'))#.order_by('-submission__uploaded_at')[:1]
    #print(aa)
    #bb = Submission.objects.annotate(max_date=Max('student__score__date'))
    #                       .filter(date=F('max_date'))

    #cc = Submission.objects.values('problem__problem_title', 'author').annotate(pb_count = Count('problem__id'))#.order_by('-uploaded_at')[:1]
    latest_problem_list = Problem.objects.order_by('-pub_date')
    my_problem_list = []
    
    print(latest_problem_list)
    for pb in Problem.objects.all():
        cc = Submission.objects.filter(author=request.user, problem=pb).order_by('-uploaded_at')[:1]
        print(cc)
        if len(cc) > 0:
            my_problem_list.append({'pb':pb, 'sm':cc[0]})
        else:
            my_problem_list.append({'pb':pb, 'sm':None})
    print(my_problem_list)
    context = {'latest_problem_list': latest_problem_list, 'my_problem_list':my_problem_list}
    return render(request, 'webgrader/index.html', context)

@login_required
def problem(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    form = SubmissionForm()
    return render(request, 'webgrader/problem.html', {'problem': problem, 'form': form})

@login_required
def submit(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    print(request.user)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, initial={'author': request.user})
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.problem = problem
            ##TODO: make grader to score the code

            form.save()
            print(form.src_code)

            # return `MEDIA_URL` + `upload_to` + absolute path of file.
            # eg; `/media/documents/filename.csv`
            print(form.src_code.url)
            return redirect('webgrader:success', problem_id=problem_id)
        else:
            print('invalid form')
            return redirect('webgrader:fail', problem_id=problem_id)
    else:
        form = SubmissionForm()
    return render(request, 'webgrader/problem.html', {'problem': problem, 'form': form})

@login_required
def success(request, problem_id):
    return render(request, 'webgrader/success.html')

@login_required
def fail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'webgrader/fail.html', {'problem': problem})