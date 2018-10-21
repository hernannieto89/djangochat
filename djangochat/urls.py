# djangochat/urls.py
"""
Urls for the DjangoChat project
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    url(r'^', include('chat.urls', namespace="chat")),
    path('admin/', admin.site.urls),
]

