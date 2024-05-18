# core/views/tutor_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def tutor(request):
    return render(request, 'core/tutor.html')

@login_required
def attendance(request):
    return render(request, 'core/attendance.html')

@login_required
def schedule(request):
    return render(request, 'core/schedule.html')

@login_required
def child(request, child_id):
    return render(request, 'core/child.html', {'child_id': child_id})
