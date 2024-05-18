# core/urls/schedule.py
from django.urls import path
from core.views import schedule_views

urlpatterns = [
    path('', schedule_views.schedule, name='schedule'),
]
