# core/views/curator_views.py
## @package core
#  Contains the view functions related to curator roles within the application.
#

## @file curator_views
#  Manages the presentation logic for curator-specific functionalities like managing tutors, children, groups, schedules, and attendance.
#

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

## Displays the main curator interface.
#  @param request The HTTP request object.
#  Renders the curator dashboard, accessible only to logged-in users.
#
@login_required
def curator(request):
    return render(request, 'core/curator.html')

## Displays the interface for adding a tutor.
#  @param request The HTTP request object.
#  Provides a form for adding new tutors, accessible only to logged-in users.
#
@login_required
def add_tutor(request):
    return render(request, 'core/add_tutor.html')

## Displays the interface for adding a child.
#  @param request The HTTP request object.
#  Provides a form for adding new children, accessible only to logged-in users.
#
@login_required
def add_child(request):
    return render(request, 'core/add_child.html')

## Displays the interface for creating a new group.
#  @param request The HTTP request object.
#  Provides a form for creating new groups, accessible only to logged-in users.
#
@login_required
def create_group(request):
    return render(request, 'core/create_group.html')

## Displays the scheduling interface for curators.
#  @param request The HTTP request object.
#  Provides a scheduling tool for managing group schedules, accessible only to logged-in users.
#
@login_required
def schedule(request):
    return render(request, 'core/schedule.html')

## Displays the attendance management interface.
#  @param request The HTTP request object.
#  Provides a tool for managing attendance records, accessible only to logged-in users.
#
@login_required
def attendance(request):
    return render(request, 'core/attendance.html')
