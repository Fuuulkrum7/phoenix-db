# core/views/tutor_views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import Worker, Group, GroupClass, Child, Course

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
    leaders, curators, volunteers = [], [], []
    children, courses = [], []

    if selected_group_id:
        selected_group = get_object_or_404(Group, pk=selected_group_id)

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
