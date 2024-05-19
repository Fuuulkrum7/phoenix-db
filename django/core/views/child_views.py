# core/views/child_views.py
## @package core
#  Contains the view functions related to children within the application.
#

## @file child_views
#  Manages the presentation logic for child-specific features such as detailed profiles, historical academic records, and contact information.
#
from django import forms
from django.utils.timezone import now

class DateRangeForm(forms.Form):
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app import models
from app.models import Child, ChildInfo, Parent, ParentPhone, ClassHistory, Group, TrackType, Visits, MarksForVisit,  MarkCategory, MarkType

## Displays detailed information about a specific child.
#  @param request The HTTP request object.
#  @param child_id The unique identifier of the child.
#  This view compiles extensive information about the child including basic info, parents' contacts, group history, upcoming lessons, and academic marks.
#  This view is protected to ensure only logged-in users can access the information.
#
@login_required
def child(request, child_id):
    child_data = Child.objects.get(child_id=child_id)
    child_info = ChildInfo.objects.filter(child=child_data)
    parents = Parent.objects.filter(child=child_data)
    parent_phones = ParentPhone.objects.filter(parent__in=parents)
    group_history = ClassHistory.objects.filter(child=child_data)
    upcoming_lessons = Visits.objects.filter(child=child_data).select_related('group_class')

    marks = MarksForVisit.objects.filter(visit__child=child_data).select_related('mark_type', 'visit')

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
        child=child_data,
        lesson_date__range=(start_date, end_date)
    ).values('visited').annotate(count=models.Count('visited'))

    skill_analysis = MarksForVisit.get_skill_analysis(child_id, start_date, end_date)
    behavior_analysis = MarksForVisit.get_behavior_analysis(child_id, start_date, end_date)

    context = {
        'child': child_data,
        'child_info': child_info,
        'parents': parents,
        'parent_phones': parent_phones,
        'group_history': group_history,
        'upcoming_lessons': upcoming_lessons,
        'marks': marks,
        'form': form,
        'attendance': attendance,
        'skill_analysis': skill_analysis,
        'behavior_analysis': behavior_analysis,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'core/child.html', context)
