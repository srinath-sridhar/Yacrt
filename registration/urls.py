from django.conf.urls import patterns, include, url
from registration import views

urlpatterns = patterns('',
                       url(r'^signin/$',views.signin_form, name="signin_form"),
                       url(r'^authenticate_user/',views.authenticate_user, name="authenticate_user"),
                       url(r'^home/',views.login_success, name="login_success"),
                       )
