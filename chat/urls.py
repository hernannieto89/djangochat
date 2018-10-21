# chat/urls.py
"""
URLS configuration for Chat App - DjangoChat project
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'chat'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^chat/(?P<room_name>[^/]+)/$', views.room_view, name='room'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^profile/$', views.update_profile, name='profile'),
]