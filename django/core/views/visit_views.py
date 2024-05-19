from django.shortcuts import render, redirect, get_object_or_404
from app.models import Visits, Child, GroupClass, Lesson
from django.utils.timezone import now
from datetime import timedelta

def add_visit(request, class_id):
    group_class = get_object_or_404(GroupClass, pk=class_id)
    group = group_class.group  # Get the associated group

    lessons = Lesson.objects.filter(class_instance_id=class_id).order_by('lesson_date')
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
            visit.clean()
            visit.save()

        return redirect('/tutor/')

    return render(request, 'core/add_visit.html', {
        'child_form_list': child_form_list,
        'group_class': group_class,
        'lessons': lessons,
    })
