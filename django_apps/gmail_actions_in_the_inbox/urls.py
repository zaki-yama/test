# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from .views import ReviewHandlerView, EmailSenderView

urlpatterns = patterns('',
    (r'^email', EmailSenderView.as_view()),
    (r'^', ReviewHandlerView.as_view()),
)
