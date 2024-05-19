# core/views/schedule_views.py
## @package core
#  Contains the view functions for scheduling within the application.
#

## @file schedule_views
#  Manages the presentation logic related to scheduling functionalities.
#

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

## Displays the scheduling interface.
#  @param request The HTTP request object.
#  This view renders the schedule management page, providing tools to manage and view various scheduling tasks.
#  Access to this view is restricted to logged-in users, ensuring that only authenticated individuals can interact with scheduling features.
#
@login_required
def schedule(request):
    return render(request, 'core/schedule.html')
