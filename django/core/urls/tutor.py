# core/urls/tutor.py
from django.urls import path
from core.views.tutor_views import tutor_view
from core.views.edit_attendance_views import *

urlpatterns = [
    path('', tutor_view, name='tutor'),
]
