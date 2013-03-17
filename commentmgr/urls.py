from django.conf.urls import patterns, include, url

from commentmgr import views

urlpatterns = patterns('', 
                       url(r'^create/$',views.create, name="create_new_comment"),
                       url(r'^edit/$', views.edit, name="edit_comment"),
                       url(r'^destroy/$', views.destroy, name="destroy_comment"),
                        url(r'^all/$', views.save, name="get_all")
                       )
