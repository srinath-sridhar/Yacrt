from django.conf.urls import patterns, include, url
from registration import views

urlpatterns = patterns('',
                       url(r'^signin/$',views.signin_form, name="signin_form"),
                       url(r'^new/$',views.create_new, name="create_new"),
                       url(r'^save$',views.save_user, name="save_user"),
                       url(r'^authenticate_user/',views.authenticate_user, name="authenticate_user"),
                       url(r'^signout/$', views.signout, name="signout")
                       )
