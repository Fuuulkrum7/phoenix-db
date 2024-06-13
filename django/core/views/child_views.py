# core/views/child_views.py

from django import forms
from django.db import models as mdls
from django.utils.timezone import now


class DateRangeForm(forms.Form):
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import (
    Child, ChildInfo, Parent, ParentPhone, ClassHistory, Course,
    Visits, MarksForVisit, ParentByChild,
    GroupClass
)

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
    child_data = Child.objects.get(child_id=child_id)
    child_info = ChildInfo.objects.filter(child_id=child_data)
    # get all parents
    parents_ids = ParentByChild.objects.values_list('parent_id', flat=True).filter(child_id=child_id)
    parents = Parent.objects.filter(parent_id__in=parents_ids)
    parents_info = [
        (parent, ParentPhone.objects.filter(parent_id=parent.parent_id)) for parent in parents
    ]
    
    group_history = ClassHistory.objects.filter(child_id=child_data)
    upcoming_lessons = Visits.objects.filter(child_id=child_data).select_related('group_class')
    marks = MarksForVisit.objects.filter(visit__child_id=child_data).select_related('mark_type', 'visit')

    # Collect courses
    course_ids = GroupClass.objects.values_list('course_id', flat=True).filter(group_id=child_data.current_group)
    courses = Course.objects.filter(course_id__in=course_ids).distinct()

    # Prepare context data for the template rendering.
    # Обработка формы выбора даты
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
        else:
            start_date = now().date()
            end_date = now().date()
    else:
        form = DateRangeForm()
        start_date = now().date()
        end_date = now().date()

    attendance = Visits.objects.filter(
        child_id=child_data,
        lesson_date__range=(start_date, end_date)
    ).values('visited').annotate(count=mdls.Count('visited'))

    skill_analysis = MarksForVisit.get_skill_analysis(child_id, start_date, end_date)
    behavior_analysis = MarksForVisit.get_behavior_analysis(child_id, start_date, end_date)

    context = {
        'child': child_data,
        'child_info': child_info,
        'parents': parents_info,
        'group_history': group_history,
        'upcoming_lessons': upcoming_lessons,
        'marks': marks,
        'courses': courses,
        'form': form,
        'attendance': attendance,
        'skill_analysis': skill_analysis,
        'behavior_analysis': behavior_analysis,
        'start_date': start_date,
        'end_date': end_date
    }

    # Render and return the template with the context data.
    return render(request, 'core/child.html', context)
