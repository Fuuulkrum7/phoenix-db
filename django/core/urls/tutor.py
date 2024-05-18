# core/urls/tutor.py
from django.urls import path
from core.views import tutor_views

urlpatterns = [
    path('', tutor_views.tutor_dashboard, name='tutor_dashboard'),
    path('attendance/', tutor_views.attendance, name='attendance'),
    path('schedule/', tutor_views.schedule, name='schedule'),
    path('child/<int:child_id>/', tutor_views.child_card, name='child_card'),
]
