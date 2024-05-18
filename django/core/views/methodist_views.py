# core/views/methodist_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def methodist_dashboard(request):
    return render(request, 'core/methodist_dashboard.html')

@login_required
def add_course(request):
    return render(request, 'core/add_course.html')

@login_required
def behavior(request):
    return render(request, 'core/behavior.html')
