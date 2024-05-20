## @package phoenixdb
#  Handles URL routing for the Django project.
#

## @file urls
#  Defines URL patterns for the phoenixdb project to direct incoming requests to appropriate views.
#

from django.contrib import admin
from django.urls import include, path
from app.views import custom_login
from django.contrib.auth import views as auth_views
from core.views.visit_views import add_visit
from django.shortcuts import redirect
# from app.views import forbidden

## List of URL patterns for the phoenixdb application.
#  This list includes paths for admin, authentication, and redirects to different sub-modules of the application.
#
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface URL.
    path('login/', custom_login, name='login'),  # Custom login view.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL using Django's built-in view.
    path('tutor/', include('core.urls.tutor')),  # Includes all URL patterns for tutor module.
    path('methodist/', include('core.urls.methodist')),  # Includes all URL patterns for methodist module.
    path('curator/', include('core.urls.curator')),  # Includes all URL patterns for curator module.
    path('tutor/attendance/', include('core.urls.attendance')),  # Includes all URL patterns for attendance module.
    path('schedule/', include('core.urls.schedule')),  # Includes all URL patterns for schedule module.
    path('child/', include('core.urls.child')),  # Includes all URL patterns for child module.
    path('statistics/', include('core.urls.statistics')),  # Includes all URL patterns for statistics module.
    path('', lambda request: redirect('login')),  # Redirects root requests to login page.
    path('add-visit/<int:class_id>/', add_visit, name='add_visit')
]
