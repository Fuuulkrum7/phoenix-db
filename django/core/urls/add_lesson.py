# core/urls/add_lesson.py
from django.urls import path
from core.views import add_lesson_views

urlpatterns = [
    path('', add_lesson_views.add_lesson, name='add_lesson'),
]
