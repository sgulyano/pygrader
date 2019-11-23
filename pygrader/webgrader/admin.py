from django.contrib import admin

# Register your models here.
from .models import Problem, Submission

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('id', 'problem_title', 'pub_date', 'max_score', 'num_test', 'visibility')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_problem', 'get_author', 'uploaded_at', 'score')

    def get_problem(self, obj):
        return obj.problem.problem_title
    get_problem.short_description = 'Problem'

    def get_author(self, obj):
        return obj.author.username
    get_author.short_description = 'Author'
#admin.site.register(Problem)
#admin.site.register(Submission)