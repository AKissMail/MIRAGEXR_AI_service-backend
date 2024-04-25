from django.contrib import admin
from django.urls import path

from speak import views as speak_views
from listen import views as listen_views
from options import views as options_views
from authentication import views as authentication_views
from think import views as think_views
from dokument import views as dokument_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('speak/', speak_views.speak, name='speak'),
    path('listen/', listen_views.listen, name="listen"),
    path('think/', think_views.think, name='think'),
    path('options/', options_views.get_options, name='options'),
    path('authentication/', authentication_views.authentication, name='authentication'),
    path('dokument/', dokument_view.dokument, name='dokument'),
    path('dokument/configuration', dokument_view.configuration, name='configuration'),
]
