# -*- coding: utf-8 -*-
from django.conf.urls import patterns

from .views import MainView, AuthView


urlpatterns = patterns('',
	(r'^oauth2callback', AuthView.as_view()),
	(r'^$', MainView.as_view()),
)
