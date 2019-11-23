from django.contrib import admin

# Register your models here.
from .models import Problem, Submission

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'

#admin.site.register(Problem)
admin.site.register(Submission)