# core/views/schedule_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from app.models import Lesson, GroupClass, Course

@login_required
def schedule(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    lessons = Lesson.objects.all()


    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        lessons = lessons.filter(lesson_date__range=(start_date, end_date))
    print("Lessons:")
    for lesson in lessons:
        print(
            f"Date: {lesson.lesson_date}, \
                Course: {lesson.class_id.course_id.course_name}, \
                Group: {lesson.class_id.group_id.group_name}")
    context = {
        'lessons': lessons,
        'start_date': start_date,
        'end_date': end_date,
        #'can_add_lesson': request.session['user_role'][0]
    }

    return render(request, 'core/schedule.html', context)
