from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('speak/', include('speak.urls')),
    path('listen/', include('listen.urls')),
    path('think/', include('think.urls')),
    path('options/', include('options.urls')),
]
