# core/urls/statistics.py
from django.urls import path
from core.views import statistics_views

urlpatterns = [
    path('', statistics_views.statistics, name='statistics'),
]
