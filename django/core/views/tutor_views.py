# core/views/tutor_views.py
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Group, Worker, Child, Course

@login_required
def tutor(request):
    return render(request, 'core/tutor.html')

@login_required
def edit_attendance(request):
    return render(request, 'core/edit_attendance.html')

@login_required
def edit_behavour(request):
    return render(request, 'core/edit_behavour.html')


@login_required
def schedule(request):
    return render(request, 'core/schedule.html')

@login_required
def child(request, child_id):
    return render(request, 'core/child.html', {'child_id': child_id})

@login_required
def leader_view(request):
    groups = Group.objects.all()
    selected_group_id = request.GET.get('group', groups.first().id if groups else None)
    selected_group = get_object_or_404(Group, id=selected_group_id)
    
    leaders = Worker.objects.filter(group=selected_group, role='leader')
    curators = Worker.objects.filter(group=selected_group, role='curator')
    volunteers = Worker.objects.filter(group=selected_group, role='volunteer')
    children = Child.objects.filter(group=selected_group)
    courses = Course.objects.filter(group=selected_group)
    
    context = {
        'groups': groups,
        'selected_group': selected_group,
        'leaders': leaders,
        'curators': curators,
        'volunteers': volunteers,
        'children': children,
        'courses': courses,
    }
    
    return render(request, 'tutor.html', context)