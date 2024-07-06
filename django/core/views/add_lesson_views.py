# core/views/add_lesson_views.py
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.db import IntegrityError

from app.models import GroupClass, Worker, Lesson, Course

## \brief basic page for adding 
@login_required
def add_lesson(request: HttpRequest) -> HttpResponse:
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or not (user_role in ['C', 'T']):
        # Handle case where user_id is not in session
        return redirect('../../login/')
    
    possible_teachers = GroupClass.objects.all().values(
        "teacher_id", "teacher_id__name", "teacher_id__surname", "teacher_id__patronymic").distinct()
    possible_courses = []
    possible_groups = []
    
    if len(possible_teachers):
        teacher = possible_teachers[0]["teacher_id"]
        possibleCourses = GroupClass.objects.filter(teacher_id=possible_teachers[0]["teacher_id"])\
                .values_list("course_id", flat=True).distinct()
        
        if len(possibleCourses):
            possible_groups = GroupClass.objects.filter(teacher_id=teacher,
                course_id=possibleCourses[0]).distinct()
    
    page_name = 'curator'
    # if user_role == 'T':
    #     page_name = 'tutor'

    context = {
        'possible_teachers': possible_teachers,
        'possible_courses': possible_courses,
        'possible_groups': possible_groups,
        'user_homepage' : page_name,
    }
    
    return render(request, 'core/add_lesson.html', context)


def validate_user(request: HttpRequest):
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or not (user_role in ['C', 'T']):
        # Handle case where user_id is not in session
        return redirect('../../../login/')


##
def get_courses_by_teacher(request: HttpRequest) -> JsonResponse:
    validate_user(request)
    
    teacher_id = request.GET["teacher-id"]

    possibleCourses = GroupClass.objects.filter(
        teacher_id=teacher_id
    ).values('course_id', 'course_id__course_name').distinct()
    
    return JsonResponse(list(possibleCourses), safe=False)


def get_groups_by_course(request: HttpRequest) -> JsonResponse:
    validate_user(request)
    
    teacher_id = request.GET["teacher-select"]
    course_id = request.GET["course-select"]
    
    possibleGroupes = GroupClass.objects.filter(
        teacher_id=teacher_id, course_id=course_id
    ).values('group_id', 'group_id__group_name').distinct()
    
    return JsonResponse(list(possibleGroupes), safe=False)

def get_teacher_lessons(request: HttpRequest) -> JsonResponse:
    validate_user(request)
    
    teacher_id = request.GET["teacher-select"]
    cur_date = datetime.strptime(request.GET["choose-date"], "%d.%m.%Y")
    
    if not teacher_id:
        messages.error(request, f'Не учитель для назначения урока')
    
    lessons_teacher = Lesson.objects.filter(
        class_id__teacher_id=teacher_id, lesson_date__date=cur_date
    ).values("lesson_date", "duration", 
             "class_id__course_id__course_name",
             "class_id__group_id__group_name")
    
    all_data = []
    
    for i in lessons_teacher:
        data = {}
        data["lesson_date"] = i["lesson_date"].date()
        data["lesson_time"] = i["lesson_date"].time()
        data["lesson_end"] = (i["lesson_date"] + timedelta(minutes=int(i["duration"]))).time()
        data["course_name"] = i["class_id__course_id__course_name"]
        data["group_name"] = i["class_id__group_id__group_name"]
        
        all_data.append(data)
    
    return JsonResponse(all_data, safe=False)

def get_group_lessons(request: HttpRequest) -> JsonResponse:
    validate_user(request)
    
    group_id = request.GET["group-select"]
    cur_date = datetime.strptime(request.GET["choose-date"], "%d.%m.%Y")
    
    if not group_id:
        messages.error(request, f'Не выбрана группа для назначения урока')
    
    lessons_group = Lesson.objects.filter(
        class_id__group_id=group_id, lesson_date__date=cur_date
    ).values("lesson_date", "duration", 
             "class_id__course_id__course_name",
             "class_id__teacher_id__name",
             "class_id__teacher_id__surname",
             "class_id__teacher_id__patronymic")
    
    all_data = []
    
    for i in lessons_group:
        data = {}
        data["lesson_date"] = i["lesson_date"].date()
        data["lesson_time"] = i["lesson_date"].time()
        data["lesson_end"] = (i["lesson_date"] + timedelta(minutes=int(i["duration"]))).time()
        data["course_name"] = i["class_id__course_id__course_name"]
        
        data["teacher_name"] = \
            f"{i['class_id__teacher_id__surname']} {i['class_id__teacher_id__name']} {i['class_id__teacher_id__patronymic']}"
        
        all_data.append(data)
    
    return JsonResponse(all_data, safe=False)


def add_new_lesson(request: HttpRequest) -> HttpResponse:
    validate_user(request)
    
    group_id = request.POST["group-select"]
    teacher_id = request.POST["teacher-select"]
    course_id = request.POST["course-select"]
    # TODO add this params (and checks for them)
    choose_date = request.POST["choose-date"]
    choose_time = request.POST["choose-time"] 
    duration = request.POST["duration"]
    
    if not group_id or not teacher_id or not course_id:
        messages.error(request, f'Не выбран один из параметров для назначения урока')
        return redirect('../')
    
    class_id = GroupClass.objects.get(
        teacher_id=teacher_id, group_id=group_id, course_id=course_id)
    
    if not class_id:
        messages.error(request, f'Некорректные параметры класса')
        return redirect('../')
    
    fact_date = datetime.strptime(choose_date + " " + choose_time, "%d.%m.%Y %H:%M")
    
    if fact_date.weekday() == 6:
        messages.error(request, f'Урок нельзя ставить на воскресенье')
        return redirect('../')
        
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
        messages.error(request, f'Происходит наложение занятий для данной группы или преподавателя')
    
    return redirect('../')
