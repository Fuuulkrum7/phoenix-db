# phoenixdb/urls.py
from django.contrib import admin
from django.urls import include, path
from app.views import custom_login
from django.contrib.auth import views as auth_views
from core.views.visit_views import add_visit
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tutor/', include('core.urls.tutor')),
    path('methodist/', include('core.urls.methodist')),
    path('curator/', include('core.urls.curator')),
    path('attendance/', include('core.urls.attendance')),
    path('schedule/', include('core.urls.schedule')),
    path('child/', include('core.urls.child')),
    path('statistics/', include('core.urls.statistics')),
    path('', lambda request: redirect('login')),
    path('add-visit/<int:class_id>/', add_visit, name='add_visit')
]
