from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/(?P<id>\d+)',views.userProfile),
    url(r'^explore$', views.explore),
<<<<<<< HEAD
    url(r'^charity$', views.displayCharity),
    url(r'^addgroup$', views.addGroup),
    url(r'^checkout$', views.checkout),
    url(r'^register$', views.register)
=======
    url(r'^statement$', views.displayStatement),
    url(r'^charity$', views.displayCharity),
    url(r'^admin/users$', views.adminUsers),
    url(r'^admin/causes$', views.adminCauses)
>>>>>>> 5c2ec322509ee8bb981bbf529344b434894f328d
]