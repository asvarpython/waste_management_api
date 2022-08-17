from posixpath import basename
from django.conf.urls import url, include
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path


urlpatterns = [
    path('', HomeApiView.as_view(),name="home"),

    
]
