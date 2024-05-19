# core/urls/tutor.py
from django.urls import path
from core.views import tutor_views

urlpatterns = [
    path('', tutor_views.tutor_view, name='tutor'),
    # path('edit_attendance/', tutor_views.edit_attendance, name='edit_attendance'),
    # path('edit_behavour/', tutor_views.edit_behavour, name='edit_behavour'),
    # path('schedule/', tutor_views.schedule, name='schedule'),
    # path('child/<int:child_id>/', tutor_views.child, name='child'),
]
