# core/views/curator_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def curator(request):
    return render(request, 'core/curator.html')

@login_required
def add_tutor(request):
    return render(request, 'core/add_tutor.html')

@login_required
def add_child(request):
    return render(request, 'core/add_child.html')

@login_required
def create_group(request):
    return render(request, 'core/create_group.html')

@login_required
def schedule(request):
    return render(request, 'core/schedule.html')

@login_required
def attendance(request):
    return render(request, 'core/attendance.html')
