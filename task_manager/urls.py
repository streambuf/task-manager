import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^tasks/', include('tasks.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


