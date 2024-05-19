# core/views/edit_lesson_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def edit_lesson(request):
    return render(request, 'core/edit_lesson.html')
