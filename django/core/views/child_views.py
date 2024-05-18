# core/views/child_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def child(request, child_id):
    # Здесь вы можете добавить логику для получения данных о ребенке
    return render(request, 'core/child.html', {'child_id': child_id})
