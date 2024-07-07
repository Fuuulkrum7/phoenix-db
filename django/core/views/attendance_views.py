from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from app.models import Course, GroupClass, Visits, Lesson
from django.contrib import messages

## \brief Displays the interface for tutors.
#  \param request The HTTP request object.
#  \return Rendered template for the tutor interface.
@login_required
def attendance_view(request):
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or not (user_role in ['T', 'C']):
        # Handle case where user_id is not in session
        return redirect('../login/') 
    
    # groups = Group.objects.all()
    courses = GroupClass.objects.values_list('course_id', flat=True).filter(teacher_id=user_id).distinct()
    selected_course = Course.objects.filter(course_id__in=courses) if courses else None
    if selected_course:
        selected_groups = GroupClass.objects.filter(
            course_id=courses.first()).values('group_id', 'group_id__group_name').distinct()
    else:
        selected_groups = []
    
    page_name = 'tutor'
    if user_role == 'C':
        page_name = 'curator'

    context = {
        'selected_course': selected_course,
        'selected_groups': selected_groups,
        'user_homepage' : page_name,
    }

    return render(request, 'core/edit_attendance.html', context)

## \brief Returns groups for a specific course.
#  \param request The HTTP request object.
#  \param course_id The ID of the course.
#  \return JSON response with the list of groups for the given course.
def get_groups_by_course(request, course_id):
    user_id = request.session.get('user_id')

    if not user_id:
        # Handle case where user_id is not in session
        return redirect('login/')
    
    groups = GroupClass.objects.filter(
        course_id=course_id, teacher_id=user_id
    ).values('group_id', 'group_id__group_name').distinct()
    
    return JsonResponse(list(groups), safe=False)

## \brief Displays the interface to add visit marks.
#  \param request The HTTP request object.
#  \param class_id The ID of the class.
#  \return Rendered template for adding visit marks.
@login_required
def get_class_id(request):
    group_id = request.GET["group-select"]
    course_id = request.GET["course-select"]
    
    if group_id is None or course_id is None:
        return redirect('attendance/')
    
    user_id = request.session.get('user_id')

    if not user_id:
        # Handle case where user_id is not in session
        return redirect('login/')
    
    class_id = GroupClass.objects.values_list('class_id', flat=True).get(
        teacher_id=user_id, group_id=group_id, course_id=course_id)
    
    # Filter out lessons that already have visits
    existing_lesson_ids = Visits.objects.filter(class_id=class_id).values_list('lesson_date', flat=True)
    lessons = Lesson.objects.filter(class_id=class_id).exclude(lesson_date__in=existing_lesson_ids)
    print(len(lessons), len(existing_lesson_ids))
    if not lessons:
        messages.error(request, f'Вся посещаемость для данной группы по данному предмету уже была отмечена ранее. '
                       'Для просмотра посещаемости перейдите в соответствующий раздел')
        return redirect('../')
    
    return redirect(str(class_id) + '/')
