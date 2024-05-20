from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Worker, Group, Child, Course, WorkerByRole, GroupClass

## Displays the interface to edit attendance records.
#  @param request The HTTP request object.
#  Only accessible to logged-in users.
#
@login_required
def tutor_view(request):
    """
    @brief Displays the interface to edit attendance records.

    This view renders the tutor interface for managing attendance. It retrieves the current user's
    worker record and the groups they lead. If a specific group is selected, it gathers detailed
    information about the group's leader, curator, children, and courses.

    @param request The HTTP request object containing metadata about the request.

    @return The rendered tutor.html page with the context data including groups, selected group,
            leader, curator, children, and courses.
    """
    # Get the current user and their worker record
    current_worker = get_object_or_404(Worker, worker_id=request.session['user_id'])
    
    # Get the groups led by the current user
    groups = Group.objects.filter(groupclass__teacher=current_worker).distinct()
    
    # Get the selected group from request parameters
    selected_group_id = request.GET.get('group')
    selected_group = None
    leader, curator = None, None
    children, courses = [], []

    if selected_group_id:
        selected_group = get_object_or_404(Group, group_id=selected_group_id)
        
        # Get the leader and curator of the selected group
        group_class = get_object_or_404(GroupClass, group=selected_group, teacher=current_worker)
        leader = group_class.teacher
        curator = WorkerByRole.objects.filter(worker=leader, level_code='C').first()
        
        # Get all children in the selected group
        children = Child.objects.filter(current_group=selected_group)
        
        # Получаем все курсы, которые проходит выбранная группа
        courses = Course.objects.filter(groupclass__group=selected_group).distinct()
    else:
        tutors = curators = children = courses = None

    # Prepare context data for the template rendering
    context = {
        'groups': groups,
        'selected_group': selected_group,
        'tutors': tutors,
        'curators': curators,
        'children': children,
        'courses': courses,
    }

    # Render and return the template with the context data
    return render(request, 'core/tutor.html', context)