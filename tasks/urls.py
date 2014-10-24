from django.conf.urls import patterns, url
from tasks import views

urlpatterns = patterns('',
	url(r'^$', views.tasks, name='tasks'),
	url(r'^delete/$', views.delete_task, name='delete_task'),
	url(r'^complete/$', views.complete_task, name='complete_task'),
)
