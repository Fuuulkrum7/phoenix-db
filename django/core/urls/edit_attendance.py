# core/urls/edit_attendance.py
from django.urls import path
from core.views import edit_attendance_views

urlpatterns = [
    path('', edit_attendance_views.edit_attendance, name='edit_attendance'),
]
