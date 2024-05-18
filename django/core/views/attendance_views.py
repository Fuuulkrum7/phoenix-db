# core/views/attendance_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def attendance(request):
    return render(request, 'core/attendance.html')
