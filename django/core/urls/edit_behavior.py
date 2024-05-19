# core/urls/edit_behavior.py
from django.urls import path
from core.views import edit_behavior_views

urlpatterns = [
    path('', edit_behavior_views.edit_behavior, name='edit_behavior'),
]
