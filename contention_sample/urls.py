from django.conf.urls import patterns, include, url
from .views import main_page

urlpatterns = patterns('',
    (r'^$', main_page),
)
