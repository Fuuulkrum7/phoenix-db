# views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Worker, WorkerByRole, Group, GroupClass, Child, Course

@login_required
def tutor_view(request):
    # Получаем текущего пользователя и его рабочую запись
    current_worker = get_object_or_404(Worker, user=request.user)
    
    # Проверяем, что пользователь является tutor
    tutor_roles = WorkerByRole.objects.filter(worker=current_worker, level_code__in=['T', 'C', 'V'])
    
    if not tutor_roles.exists():
        # Если у пользователя нет нужной роли, то перенаправляем или возвращаем ошибку
        return render(request, 'core/not_authorized.html')
    
    # Получаем группы, которыми руководит текущий пользователь
    groups = Group.objects.filter(groupclass__teacher=current_worker).distinct()
    
    # Получаем выбранную группу из параметров запроса
    selected_group_id = request.GET.get('group')
    selected_group = None
    leaders, curators, volunteers = [], [], []
    children, courses = [], []

    if selected_group_id:
        selected_group = get_object_or_404(Group, id=selected_group_id)
        
        # Получаем всех tutor выбранной группы
        group_classes = GroupClass.objects.filter(group=selected_group)
        leaders = group_classes.filter(teacher__workerbyrole__level_code='L')
        curators = group_classes.filter(teacher__workerbyrole__level_code='C')
        volunteers = group_classes.filter(teacher__workerbyrole__level_code='V')
        
        # Получаем всех детей в выбранной группе
        children = Child.objects.filter(current_group=selected_group)
        
        # Получаем все курсы, которые проходит выбранная группа
        courses = Course.objects.filter(groupclass__group=selected_group).distinct()

    context = {
        'groups': groups,
        'selected_group': selected_group,
        'leaders': leaders,
        'curators': curators,
        'volunteers': volunteers,
        'children': children,
        'courses': courses
    }

    return render(request, 'core/tutor.html', context)