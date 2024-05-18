# core/urls/methodist.py
from django.urls import path
from core.views import methodist_views

urlpatterns = [
    path('', methodist_views.methodist, name='methodist'),
    path('add_course/', methodist_views.add_course, name='add_course'),
    path('behavior/', methodist_views.behavior, name='behavior'),
]
