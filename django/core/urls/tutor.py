# core/urls/tutor.py
from django.urls import path
from core.views.tutor_views import tutor_view

urlpatterns = [
    path('', tutor_view, name='tutor'),
]
