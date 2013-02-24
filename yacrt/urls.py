from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from registration import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Yacrt.views.home', name='home'),
    # url(r'^Yacrt/', include('Yacrt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$',views.signin_form),
    url(r'^registration/', include('registration.urls')),
    url(r'^repos/', include('repobrowser.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
