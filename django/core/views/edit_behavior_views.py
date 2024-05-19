# core/views/edit_behavior_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def edit_behavior(request):
    return render(request, 'core/edit_behavior.html')
