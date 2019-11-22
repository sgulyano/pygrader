from django.shortcuts import get_object_or_404, render, redirect
from .models import Problem
#from .form import SubmissionForm
from .forms import SubmissionForm

def index(request):
    latest_problem_list = Problem.objects.order_by('-pub_date')
    context = {'latest_problem_list': latest_problem_list}
    return render(request, 'webgrader/index.html', context)

def problem(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    form = SubmissionForm()
    return render(request, 'webgrader/problem.html', {'problem': problem, 'form': form})  



def submit(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    print(request.user)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, initial={'author': request.user})
        if form.is_valid():
            print('form valid')
            print(form.data['author'])
            # file is saved
            form.save()
            return redirect('webgrader:index')
        else:
            print('invalid form')
    else:
        form = SubmissionForm()
    return render(request, 'webgrader/problem.html', {'problem': problem, 'form': form})

# def submit(request, problem_id):
#     problem = get_object_or_404(Problem, pk=problem_id)
    
#     if request.method == 'POST':
#         form = SubmissionForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('webgrader:index')
#         else:
#             print('Submit Error')
#     else:
#         form = SubmissionForm()
#         return render(request, 'webgrader/problem.html', {'problem': problem, 'form': form})
#     return redirect('webgrader:index')
    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))