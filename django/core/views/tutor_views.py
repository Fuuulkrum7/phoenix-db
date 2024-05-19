# core/views/tutor_views.py

## @package core
#  Contains the view functions for the tutor roles within the application.
#

## @file tutor_views
#  Manages the presentation logic for tutor-specific features like group management, attendance, behavior editing, and schedules.
#

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from app.models import Worker, WorkerByRole, Group, GroupClass, Child, Course

## Displays the main tutor interface.
#  @param request The HTTP request object.
#  Retrieves the tutor's associated groups, selected group details, leaders, curators, volunteers, children in the group, and courses.
#  Redirects to login if the user is not authenticated or session information is missing.
#
@login_required
def tutor_view(request):
    # Получаем текущего пользователя и его рабочую запись из сессии
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    if not user_id:
        return redirect('login')

    current_worker = get_object_or_404(Worker, pk=user_id)

    # Получаем группы, которыми руководит текущий пользователь
    groups = Group.objects.filter(groupclass__teacher=current_worker).distinct()

    # Получаем выбранную группу из параметров запроса
    selected_group_id = request.GET.get('group')
    selected_group = None
    leader, curator = None, None
    children, courses = [], []

    if selected_group_id:
        selected_group = get_object_or_404(Group, group_id=selected_group_id)
        
        # Получаем лидера и куратора выбранной группы
        group_class = get_object_or_404(GroupClass, group=selected_group, teacher=current_worker)
        leader = group_class.teacher
        curator = WorkerByRole.objects.filter(worker=leader, level_code='C').first()
        
        # Получаем всех детей в выбранной группе
        children = Child.objects.filter(current_group=selected_group)

        # Получаем все курсы, которые проходит выбранная группа
        courses = Course.objects.filter(groupclass__group=selected_group).distinct()

    context = {
        'groups': groups,
        'selected_group': selected_group,
        'leader': leader,
        'curator': curator,
        'children': children,
        'courses': courses
    }

    return render(request, 'core/tutor.html', context)

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
    child = get_object_or_404(Child, pk=child_id)
    return render(request, 'core/child.html', {'child': child})
