# core/views/schedule_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def schedule(request):
    return render(request, 'core/schedule.html')
