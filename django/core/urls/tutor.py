# core/urls/tutor.py
from django.urls import path
from core.views import tutor_views

urlpatterns = [
    path('', tutor_views.tutor, name='tutor'),
    path('attendance/', tutor_views.attendance, name='attendance'),
    path('schedule/', tutor_views.schedule, name='schedule'),
    path('child/<int:child_id>/', tutor_views.child, name='child'),
]
