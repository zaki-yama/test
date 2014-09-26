from django.conf.urls import patterns
from django.views.generic import TemplateView
from .views import CsrfView1, CsrfView2, CsrfView3

urlpatterns = patterns('',
	(r'^view1/', CsrfView1.as_view()),
	(r'^view2/', CsrfView2.as_view()),
	(r'^view3/', CsrfView3.as_view()),
	(r'^', TemplateView.as_view(template_name='template.html')),
)
