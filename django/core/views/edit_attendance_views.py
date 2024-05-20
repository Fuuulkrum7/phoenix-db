from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from app.models import Worker, Group, Child, Course, WorkerByRole, GroupClass

## \brief Displays the interface for tutors.
#  \param request The HTTP request object.
#  \return Rendered template for the tutor interface.
@login_required
def tutor_view(request):
    user_id = request.session.get('user_id')

    if not user_id:
        # Handle case where user_id is not in session
        return redirect('/login') 
    
    # groups = Group.objects.all()
    courses = Course.objects.all()  # Fetch all courses

    selected_course_id = request.GET.get('course')
    selected_course = get_object_or_404(Course, course_id=selected_course_id) if selected_course_id else None

    if selected_course:
        selected_groups = GroupClass.objects.filter(course=selected_course).values('group_id', 'group__group_name')
    else:
        selected_groups = []

    context = {
        'courses': courses,
        'selected_course': selected_course,
        'selected_groups': selected_groups,
    }

    return render(request, 'core/edit_attendance.html', context)

## \brief Returns groups for a specific course.
#  \param request The HTTP request object.
#  \param course_id The ID of the course.
#  \return JSON response with the list of groups for the given course.
def get_groups_by_course(request, course_id):
    groups = GroupClass.objects.filter(course_id=course_id).values('group_id', 'group__group_name')
    return JsonResponse(list(groups), safe=False)

## \brief Displays the interface to add visit marks.
#  \param request The HTTP request object.
#  \param class_id The ID of the class.
#  \return Rendered template for adding visit marks.
@login_required
def add_visit_marks_view(request, class_id):
    group_class = get_object_or_404(GroupClass, class_id=class_id)
    return render(request, 'core/add_visit_marks.html', {'group_class': group_class})
