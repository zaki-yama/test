# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from django.core.context_processors import csrf

from .models import MyModel


import logging
logger = logging.getLogger(name='hoge')

def main_page(request):
	logger.info(':::::::::::::::::::::::::')

	MyModel.upsert_multi(10)
	template_values = Context({})
	template_values.update(csrf(request))
	return HttpResponse(loader.get_template('contention_sample/main_page.html').render(template_values))
