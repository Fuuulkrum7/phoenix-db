# core/views/add_course_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def add_course(request):
    return render(request, 'core/add_course.html')
