# core/urls/curator.py
from django.urls import path
from core.views import curator_views

urlpatterns = [
    path('', curator_views.curator, name='curator'),
    path('add_tutor/', curator_views.add_tutor, name='add_tutor'),
    path('add_child/', curator_views.add_child, name='add_child'),
    path('add_group/', curator_views.add_group, name='add_group'),
    path('schedule/', curator_views.schedule, name='schedule'),
    path('attendance/', curator_views.attendance, name='curator_attendance'),
]
