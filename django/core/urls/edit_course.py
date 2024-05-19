# core/urls/edit_course.py
from django.urls import path
from core.views import edit_course_views

urlpatterns = [
    path('', edit_course_views.edit_course, name='edit_course'),
]
