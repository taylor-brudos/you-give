from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^explore$', views.explore),
    url(r'^charity$', views.displayCharity),
]