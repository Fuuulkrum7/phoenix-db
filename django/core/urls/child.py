# core/urls/child.py
from django.urls import path
from core.views import child_views

urlpatterns = [
    path('<int:child_id>/', child_views.child, name='child'),
]
