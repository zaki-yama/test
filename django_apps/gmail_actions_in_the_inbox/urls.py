# -*- coding: utf-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^$', ReviewHandlerView.as_view()),
    (r'^sign/$', sign_post),
)
