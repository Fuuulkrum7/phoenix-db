# core/views/tutor_views.py
## @package core
#  Contains the view functions for the tutor roles within the application.
#

## @file tutor_views
#  Manages the presentation logic for tutor-specific features like group management, attendance, behavior editing, and schedules.
#

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import Worker, Group, GroupClass, Child, Course

## Displays the main tutor interface.
#  @param request The HTTP request object.
#  Retrieves the tutor's associated groups, selected group details, leaders, curators, volunteers, children in the group, and courses.
#  Redirects to login if the user is not authenticated or session information is missing.
#
@login_required
def tutor_view(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    if not user_id:
        return redirect('login')

    current_worker = get_object_or_404(Worker, pk=user_id)
    groups = Group.objects.filter(groupclass__teacher=current_worker).distinct()
    selected_group_id = request.GET.get('group')
    selected_group = None
    leaders, curators, volunteers = [], [], []
    children, courses = [], []

    if selected_group_id:
        selected_group = get_object_or_404(Group, pk=selected_group_id)
        group_classes = GroupClass.objects.filter(group=selected_group)
        leaders = group_classes.filter(teacher__workerbyrole__level_code='L')
        curators = group_classes.filter(teacher__workerbyrole__level_code='C')
        volunteers = group_classes.filter(teacher__workerbyrole__level_code='V')
        children = Child.objects.filter(current_group=selected_group)
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

## Displays the interface to edit attendance records.
#  @param request The HTTP request object.
#  Only accessible to logged-in users.
#
@login_required
def edit_attendance(request):
    return render(request, 'core/edit_attendance.html')

## Displays the interface to edit behavior records.
#  @param request The HTTP request object.
#  Only accessible to logged-in users.
#
@login_required
def edit_behavour(request):
    return render(request, 'core/edit_behavour.html')

## Displays the scheduling interface for tutors.
#  @param request The HTTP request object.
#  Only accessible to logged-in users.
#
@login_required
def schedule(request):
    return render(request, 'core/schedule.html')

## Displays detailed information about a specific child.
#  @param request The HTTP request object.
#  @param child_id The unique identifier of the child.
#  Only accessible to logged-in users.
#
@login_required
def child(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    return render(request, 'core/child.html', {'child': child})
