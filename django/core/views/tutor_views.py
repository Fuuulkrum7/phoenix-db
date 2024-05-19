# core/views/tutor_views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from app.models import Worker, WorkerByRole, Group, GroupClass, Child, Course

## Displays the interface to edit attendance records.
#  @param request The HTTP request object.
#  Only accessible to logged-in users.
#
@login_required
def tutor_view(request):
    # Получаем текущего пользователя и его рабочую запись
    current_worker = get_object_or_404(Worker, worker_id=request.session['user_id'])
    
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
