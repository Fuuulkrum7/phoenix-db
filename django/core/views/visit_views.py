from django.shortcuts import render, redirect, get_object_or_404
from app.models import Visits, Child, GroupClass, Lesson
from django.utils.timezone import now
from django.db import IntegrityError
from django.contrib import messages

from datetime import timedelta

def add_visit(request, class_id):
    user_id = request.session.get('user_id')
    
    user_role = request.session.get('user_role')
    if not (user_role in ['T', 'C']):
        messages.error(request, 'Доступ запрещен. Вы не преподаватель/куратор.')
        if user_role == 'M':
            return redirect('../methodist')
        return redirect('../login')


    if not user_id:
        # Handle case where user_id is not in session
        return redirect('../login/') 
    
    group_class = get_object_or_404(GroupClass, pk=class_id)
    group = group_class.group  # Get the associated group
    
    # Filter out lessons that already have visits
    existing_lesson_ids = Visits.objects.filter(group_class=group_class).values_list('lesson_date', flat=True)
    lessons = Lesson.objects.filter(class_instance=group_class).exclude(lesson_date__in=existing_lesson_ids)

    for lesson in lessons:
        lesson.end_time = lesson.lesson_date + timedelta(minutes=lesson.duration)

    children = Child.objects.filter(current_group=group)
    child_form_list = [{'child': child} for child in children]

    if request.method == 'POST':
        lesson_id = request.POST.get('lesson')
        lesson = get_object_or_404(Lesson, pk=lesson_id)

        for child in children:
            visited = request.POST.get(f'visited_{child.child_id}') == 'on'
            print(request.POST.get(f'description_{child.child_id}'))
            description = request.POST.get(f'description_{child.child_id}', '') if not visited else ''

            visit = Visits(
                child_id=child.child_id,
                group_class_id=class_id,
                lesson_date=lesson.lesson_date,
                description=description,
                visited=visited
            )
            try:
                visit.clean()
                visit.save()
            except IntegrityError as e:
                print(e)
                messages.error(request, f'Посещаемость для данного урока уже была отмечена ранее.')
                return redirect('add_visit', class_id=class_id)
        # if we are adding last lesson, let's go back to all lessons
        if len(lessons) == 1:
            return redirect('../..')
        
        return redirect('add_visit', class_id=class_id)

    return render(request, 'core/add_visit.html', {
        'child_form_list': child_form_list,
        'group_class': group_class,
        'lessons': lessons,
    })
