from django.conf.urls import patterns, include, url

from repobrowser import views

urlpatterns = patterns('', 
                       url(r'^home/$',views.repos_home, name="repos_home"),
                       url(r'^revisions/$', views.get_repo_revisions, name="repos_revisions"),
                       url(r'^revisions/changes/$', views.get_revision_changes, name="repos_revisions_changes"),
                        url(r'^save/$', views.save, name="repos_save")
                       )
