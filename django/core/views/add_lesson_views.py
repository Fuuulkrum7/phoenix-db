# core/views/add_lesson_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def add_lesson(request):
    return render(request, 'core/add_lesson.html')
