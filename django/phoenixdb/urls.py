# phoenixdb/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tutor/', include('core.urls.tutor')),
    path('methodist/', include('core.urls.methodist')),
    path('curator/', include('core.urls.curator')),
    path('attendance/', include('core.urls.attendance')),
    path('schedule/', include('core.urls.schedule')),
    path('child/', include('core.urls.child')),
    path('statistics/', include('core.urls.statistics')),
]
