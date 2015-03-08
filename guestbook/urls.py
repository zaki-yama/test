from django.conf.urls import patterns, include, url

from .views import MainView, PostView


urlpatterns = patterns('',
	(r'^sign/$', PostView.as_view()),
	(r'^$', MainView.as_view()),
)
