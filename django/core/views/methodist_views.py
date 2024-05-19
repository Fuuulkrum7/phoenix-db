# core/views/methodist_views.py
## @package core
#  Contains the view functions for methodist roles within the application.
#

## @file methodist_views
#  Manages the presentation logic for methodist-specific functionalities, including course management and behavior tracking.
#

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course
from .forms import CourseForm
from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'group']

## Displays the main methodist interface.
#  @param request The HTTP request object.
#  Renders the methodist dashboard, which provides access to various methodist functionalities, accessible only to logged-in users.
#
@login_required
def methodist_view(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'methodist.html', context)


## Displays the interface for adding a new course.
#  @param request The HTTP request object.
#  Provides a form for methodists to add new courses to the curriculum, accessible only to logged-in users.
#
@login_required
def add_course_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('methodist')
    else:
        form = CourseForm()

    return render(request, 'add_course.html', {'form': form})

## Displays the behavior management interface.
#  @param request The HTTP request object.
#  Provides tools for monitoring and managing student behavior, accessible only to logged-in users.
#
@login_required
def edit_course_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('methodist')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'edit_course.html', {'form': form, 'course': course})


