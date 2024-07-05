# core/views/add_lesson_views.py
from datetime import datetime
import locale

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.db import IntegrityError

from app.models import GroupClass, Semester, Lesson

## \brief basic page for adding 
@login_required
def add_lesson(request: HttpRequest) -> HttpResponse:
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or not (user_role in ['C']):
        # Handle case where user_id is not in session
        return redirect('../../login/')
    
    possible_teachers = GroupClass.objects.all().values("teacher_id", flat=True)
    possible_courses = []
    possible_groups = []
    
    if len(possible_teachers):
        possibleCourses = GroupClass.objects.filter(teacher_id=possible_teachers[0])
        
    if len(possibleCourses):
        possible_groups = GroupClass.objects.filter(course_id=possibleCourses[0])
    
    page_name = 'curator'
    # if user_role == 'T':
    #     page_name = 'tutor'

    context = {
        'possible_teachers': possible_teachers,
        'possible_courses': possible_courses,
        'possible_groups': possible_groups,
        'user_homepage' : page_name,
    }
    
    return render(request, 'core/add_lesson.html')


##
def get_courses_by_teacher(request: HttpRequest, teacher_id: int) -> JsonResponse:
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or not (user_role in ['C']):
        # Handle case where user_id is not in session
        return redirect('../../../../login/')

    possibleCourses = GroupClass.objects.filter(
        teacher_id=teacher_id
    ).values('course_id', 'course_id__course_name').distinct()
    
    return JsonResponse(list(possibleCourses), safe=False)

def get_groups_by_course(request: HttpRequest, teacher_id: int, course_id: int) -> JsonResponse:
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or not (user_role in ['C']):
        # Handle case where user_id is not in session
        return redirect('../../../../login/')
    
    
    possibleGroupes = GroupClass.objects.filter(
        teacher_id=teacher_id, course_id=course_id
    ).values('group_id', 'group_id__group_name').distinct()
    
    return JsonResponse(list(possibleGroupes), safe=False)

def add_lesson_with_data(request: HttpRequest) -> HttpResponse:
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or not (user_role in ['C']):
        # Handle case where user_id is not in session
        return redirect('../../../login/')
    
    group_id = request.POST["group-select"]
    teacher_id = request.POST["teacher-select"]
    course_id = request.POST["course-select"]
    # TODO add this params (and checks for them)
    choose_date = request.POST["choose-date"]
    choose_time = request.POST["choose-time"] 
    duration = request.POST["duration"]
    
    if group_id is None or course_id is None or teacher_id is None:
        return redirect('add_lesson')
    
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    fact_date = datetime.strptime(choose_date + " " + choose_time, "%d %b %Y %H:%M")
    
    class_id = GroupClass.objects.values_list('class_id', flat=True).get(
        teacher_id=teacher_id, group_id=group_id, course_id=course_id)
    
    lesson = Lesson(
        duration=duration,
        lesson_date=fact_date,
        class_id=class_id
    )
    
    try:
        lesson.clean()
        lesson.save()
    except IntegrityError as e:
        print(e)
        messages.error(request, f'Некорректные параметры для занятия')
        return redirect('add_visit', class_id=class_id)
