# core/views/schedule_views.py
from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from app.models import Lesson, GroupClass, Semester

@login_required
def schedule(request):
    user_id = request.session['user_id']
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # When we haven't got one of this dates, set it
    if not (start_date and end_date):
        try:
            cur_semester = Semester.objects.get(start_date__lte=date.today(), end_date__gte=date.today())
            start_date = start_date if start_date else date.today()
            end_date = end_date if end_date else cur_semester.end_date
        except Exception as e:
            print(e)
        
    classes = GroupClass.objects.filter(teacher_id=user_id).select_related('group_class')
    lessons = Lesson.objects.filter(class_id__in=classes)


    if start_date and end_date:
        if isinstance(start_date, str):
            start_date = parse_date(start_date)
        if isinstance(end_date, str):
            end_date = parse_date(end_date)
        
        lessons = lessons.filter(lesson_date__range=(start_date, end_date))
    
    context = {
        'lessons': lessons,
        'start_date': start_date,
        'end_date': end_date,
        'can_add_lesson': request.session['user_role'] == 'T'
    }

    return render(request, 'core/schedule.html', context)
