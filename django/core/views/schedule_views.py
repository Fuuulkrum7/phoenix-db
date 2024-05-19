# core/views/schedule_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from app.models import Lesson

@login_required
def schedule(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    lessons = Lesson.objects.all()

    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        lessons = lessons.filter(lesson_date__range=(start_date, end_date))

    context = {
        'lessons': lessons,
        'start_date': start_date,
        'end_date': end_date,
        'can_add_lesson': request.session['user_roles'][0]
    }

    return render(request, 'core/schedule.html', context)
