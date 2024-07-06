# core/urls/schedule.py
from django.urls import path,  include
from core.views import schedule_views, add_lesson_views, edit_lesson_views

urlpatterns = [
    path('schedule/', schedule_views.schedule, name='schedule'),
    path('add_lesson/', add_lesson_views.add_lesson, name='add_lesson'),
    path('add_lesson/add_new_lesson/', add_lesson_views.add_new_lesson, name='add_new_lesson'),
    path('add_lesson/get-courses/', add_lesson_views.get_courses_by_teacher, name='get_courses_by_teacher'),
    path('add_lesson/get-groups/', add_lesson_views.get_groups_by_course, name='get_groups_by_course'),
    path('add_lesson/get-teacher-lessons/', add_lesson_views.get_teacher_lessons, name='get_teacher_lessons'),
    path('add_lesson/get-group-lessons/', add_lesson_views.get_group_lessons, name='get_group_lessons'),
    path('edit_lesson/', edit_lesson_views.edit_lesson, name='edit_lesson'),
]
