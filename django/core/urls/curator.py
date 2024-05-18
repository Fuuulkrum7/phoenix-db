# core/urls/curator.py
from django.urls import path
from core.views import curator_views

urlpatterns = [
    path('', curator_views.curator, name='curator'),
    path('add_tutor/', curator_views.add_tutor, name='add_tutor'),
    path('add_child/', curator_views.add_child, name='add_child'),
    path('create_group/', curator_views.create_group, name='create_group'),
    path('schedule/', curator_views.schedule, name='curator_schedule'),
    path('attendance/', curator_views.attendance, name='curator_attendance'),
]
