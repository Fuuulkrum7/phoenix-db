# core/urls/add_course.py
from django.urls import path
from core.views import add_course_views

urlpatterns = [
    path('', add_course_views.add_course, name='add_course'),
]
