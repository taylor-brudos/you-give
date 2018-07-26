from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/(?P<id>\d+)',views.userProfile),
    url(r'^explore$', views.explore),
    url(r'^addgroup$', views.addGroup),
    url(r'^checkout$', views.checkout),
    url(r'^register$', views.register),
    url(r'^statement$', views.displayStatement),
    url(r'^admin/users$', views.adminUsers),
    url(r'^admin/causes$', views.adminCauses),
    url(r'^charity/(?P<cause_id>\d+)$', views.displayCharity),
    url(r'^admin/users$', views.adminUsers),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^registeruser$', views.registerUser),
    url(r'^deleteuser$', views.deleteUser),
    url(r'^updateuser$', views.updateUser),
    url(r'^adduser$', views.addUser),
    url(r'^deletecause$', views.deleteCause),
    url(r'^updatecause$', views.updateCause),
    url(r'^addcause$', views.addCause),
]
