# core/urls/attendance.py
from django.urls import path
from core.views import attendance_views

urlpatterns = [
    path('', attendance_views.attendance, name='attendance'),
]
