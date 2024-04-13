from django.contrib import admin
from django.urls import path, include

from backend.speak import views as speak_views
from backend.listen import views as listen_views
from backend.options import views as options_views
from backend.authentication import views as authentication_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('speak/', speak_views.speak),
    path('listen/', listen_views.listen),
    path('think/', include('think.urls')),
    path('options/', options_views.get_options),
    path('authentication/', authentication_views.authentication),
]
