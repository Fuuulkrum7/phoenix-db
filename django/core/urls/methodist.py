# core/urls/methodist.py
from django.urls import path
from . import views

urlpatterns = [
    path('methodist/', views.methodist_view, name='methodist'),
    path('add_course/', views.add_course_view, name='add_course'),
    path('edit_course/<int:pk>/', views.edit_course_view, name='edit_course'),
]
