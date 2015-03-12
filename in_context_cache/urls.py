from django.conf.urls import patterns, include, url

from .views import MainView


urlpatterns = patterns('',
	(r'^$', MainView.as_view()),
)
