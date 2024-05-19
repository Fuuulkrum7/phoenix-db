# core/views/child_views.py
## @package core
#  Contains the view functions related to children within the application.
#

## @file child_views
#  Manages the presentation logic for child-specific features such as detailed profiles, historical academic records, and contact information.
#

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Child, ChildInfo, Parent, ParentPhone, ClassHistory, Group, TrackType, Visits, MarksForVisit, VisitType, MarkCategory, MarkType

## Displays detailed information about a specific child.
#  @param request The HTTP request object.
#  @param child_id The unique identifier of the child.
#  This view compiles extensive information about the child including basic info, parents' contacts, group history, upcoming lessons, and academic marks.
#  This view is protected to ensure only logged-in users can access the information.
#
@login_required
def child(request, child_id):
    # Fetch the main child record.
    child_data = Child.objects.get(child_id=child_id)

    # Collect related information from other tables by child object.
    child_info = ChildInfo.objects.filter(child=child_data)
    parents = Parent.objects.filter(child=child_data)
    parent_phones = ParentPhone.objects.filter(parent__in=parents)
    group_history = ClassHistory.objects.filter(child=child_data)
    upcoming_lessons = Visits.objects.filter(child=child_data).select_related('group_class')
    marks = MarksForVisit.objects.filter(visit__child=child_data).select_related('mark_type', 'visit')

    # Prepare context data for the template rendering.
    context = {
        'child': child_data,
        'child_info': child_info,
        'parents': parents,
        'parent_phones': parent_phones,
        'group_history': group_history,
        'upcoming_lessons': upcoming_lessons,
        'marks': marks
    }

    # Render and return the template with the context data.
    return render(request, 'core/child.html', context)
