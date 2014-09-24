# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from .views import ReviewHandlerView, EmailSenderView

urlpatterns = patterns('',
    (r'^', ReviewHandlerView.as_view()),
    (r'^email/', EmailSenderView.as_view()),
)
