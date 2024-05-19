# core/views/edit_course_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def edit_course(request):
    return render(request, 'core/edit_course.html')
