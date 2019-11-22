from django.urls import path

from . import views

app_name = 'webgrader'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:problem_id>/', views.problem, name='problem'),
    path('<int:problem_id>/submit/', views.submit, name='submit'),
]