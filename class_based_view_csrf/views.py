# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.decorators import method_decorator


class CsrfView1(View):

	def post(self, request):
		return HttpResponse('ok')


class CsrfView2(View):

	def post(self, request):
		return HttpResponse('ok')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(CsrfView2, self).dispatch(*args, **kwargs)


class CsrfView3(View):

	def post(self, request):
		return HttpResponse('ok')

	# This also works
	@csrf_exempt
	def dispatch(self, *args, **kwargs):
		return super(CsrfView3, self).dispatch(*args, **kwargs)
