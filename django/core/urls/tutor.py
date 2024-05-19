# core/urls/tutor.py
from django.urls import path
from core.views.tutor_views import tutor

urlpatterns = [
    path('', tutor, name='tutor'),
]
