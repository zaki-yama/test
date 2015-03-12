# -*- encoding: utf-8 -*-
import urllib

from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.views.generic import View

from google.appengine.ext import ndb

from .models import MyModel


class MainView(View):
	template_name = 'in_context_cache/index.html'

	def get(self, request):
		ctx = ndb.get_context()
		# ctx.set_cache_policy(False)  # In-Context Cache を無効にしたい場合
		ctx.set_memcache_policy(False)  # Memcache を無効にしたい場合
		ctx.set_cache_policy(lambda key: key.kind() != 'MyModel')

		key = ndb.Key(MyModel, 'foo')
		model1 = key.get()
		model2 = key.get()
		model3 = key.get()
		model4 = key.get()
		model5 = key.get()

		for i in xrange(1000):
			x = 1
			model5 = key.get()

		template_values = {
				'model': model1,
				}
		template_values.update(csrf(request))
		return render(request, self.template_name, template_values)
