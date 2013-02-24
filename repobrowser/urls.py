from django.conf.urls import patterns, include, url

from repobrowser import views

urlpatterns = patterns('', 
                       url(r'^home/$',views.repos_home, name="repos_home"),
                       )
