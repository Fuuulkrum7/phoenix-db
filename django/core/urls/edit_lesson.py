# core/urls/edit_lesson.py
from django.urls import path
from core.views import edit_lesson_views

urlpatterns = [
    path('', edit_lesson_views.edit_lesson, name='edit_lesson'),
]
