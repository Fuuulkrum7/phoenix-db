from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import Worker, Group, Child, Course, WorkerByRole, GroupClass

## Displays the interface to edit attendance records.
#  @param request The HTTP request object.
#  Only accessible to logged-in users.
#
@login_required
def tutor_view(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        # Handle case where user_id is not in session
        return redirect('/login') 

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
