# core/views/tutor_views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Worker, Group, Child, Course, WorkerByRole

## Displays the main tutor interface.
#  @param request The HTTP request object.
#  Retrieves the tutor's associated groups, selected group details, leaders, curators, volunteers, children in the group, and courses.
#  Redirects to login if the user is not authenticated or session information is missing.
#
@login_required
def tutor(request):
    user_id = request.session.get('user_id')

    groups = Group.objects.all()

    selected_group_id = request.GET.get('group', groups.first().group_id if groups else None)
    selected_group = get_object_or_404(Group, group_id=selected_group_id) if selected_group_id else None

    if selected_group:
        tutors = WorkerByRole.objects.filter(worker__groupcreators__group=selected_group, level_code='T')
        curators = WorkerByRole.objects.filter(worker__groupcreators__group=selected_group, level_code='C')
        children = Child.objects.filter(current_group=selected_group)
        courses = Course.objects.filter(groupclass__group=selected_group).distinct()
    else:
        tutors = curators = children = courses = None

    context = {
        'groups': groups,
        'selected_group': selected_group,
        'tutors': tutors,
        'curators': curators,
        'children': children,
        'courses': courses,
    }

    return render(request, 'core/tutor.html', context)
