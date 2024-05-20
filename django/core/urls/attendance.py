# core/urls/attendance.py
from django.urls import path
from core.views.attendance_views import *
from core.views.visit_views import add_visit

urlpatterns = [
    path('', attendance_view, name='attendance'),
    path('get-groups/<int:course_id>/', get_groups_by_course, name='get_groups_by_course'),
    path('add-visit/', get_class_id),
    path('add-visit/<int:class_id>/', add_visit, name='add_visit')
]
