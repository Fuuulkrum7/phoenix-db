# core/views/child_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Child, ChildInfo, Parent, ParentPhone, ClassHistory, Group, TrackType, Visits, MarksForVisit, VisitType, MarkCategory, MarkType

@login_required
def child(request, child_id):
    child_data = Child.objects.get(child_id=child_id)
    child_info = ChildInfo.objects.filter(child=child_data)
    parents = Parent.objects.filter(child=child_data)
    parent_phones = ParentPhone.objects.filter(parent__in=parents)
    group_history = ClassHistory.objects.filter(child=child_data)
    upcoming_lessons = Visits.objects.filter(child=child_data).select_related('group_class')

    marks = MarksForVisit.objects.filter(visit__child=child_data).select_related('mark_type', 'visit')

    context = {
        'child': child_data,
        'child_info': child_info,
        'parents': parents,
        'parent_phones': parent_phones,
        'group_history': group_history,
        'upcoming_lessons': upcoming_lessons,
        'marks': marks
    }

    return render(request, 'core/child.html', context)
