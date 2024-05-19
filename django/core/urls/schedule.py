# core/urls/schedule.py
from django.urls import path
from core.views import schedule_views, add_lesson_views, edit_lesson_views

urlpatterns = [
    path('schedule/', schedule_views.schedule, name='schedule'),
    path('add_lesson/', add_lesson_views.add_lesson, name='add_lesson'),
    path('edit_lesson/', edit_lesson_views.edit_lesson, name='edit_lesson'),
]
