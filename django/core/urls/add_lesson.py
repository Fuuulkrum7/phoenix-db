# core/urls/add_lesson.py
from django.urls import path
from core.views import add_lesson_views

urlpatterns = [
    path('', add_lesson_views.add_lesson, name='add_lesson'),
    path('get-courses/<int:teacher_id>/', add_lesson_views.get_courses_by_teacher, name='get_courses_by_teacher'),
    path('get-groups/<int:course_id>/', add_lesson_views.get_groups_by_course, name='get_groups_by_course'),
    path('add_new_lesson/', add_lesson_views.add_lesson_with_data),
]
