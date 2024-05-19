# core/views/methodist_views.py
## @package core
#  Contains the view functions for methodist roles within the application.
#

## @file methodist_views
#  Manages the presentation logic for methodist-specific functionalities, including course management and behavior tracking.
#

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

## Displays the main methodist interface.
#  @param request The HTTP request object.
#  Renders the methodist dashboard, which provides access to various methodist functionalities, accessible only to logged-in users.
#
@login_required
def methodist(request):
    return render(request, 'core/methodist.html')

## Displays the interface for adding a new course.
#  @param request The HTTP request object.
#  Provides a form for methodists to add new courses to the curriculum, accessible only to logged-in users.
#
@login_required
def add_course(request):
    return render(request, 'core/add_course.html')

## Displays the behavior management interface.
#  @param request The HTTP request object.
#  Provides tools for monitoring and managing student behavior, accessible only to logged-in users.
#
@login_required
def behavior(request):
    return render(request, 'core/behavior.html')
