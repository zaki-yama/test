# -*- coding: utf-8 -*-
from django.http import HttpResponsePermanentRedirect
from google.appengine.api import users


def login_required(handler_method):
	u"""Django の Class-based View 用デコレータ
	ref. appengine/ext/webapp/util.py

	Example:
		class MyView(View):

			@login_required
			def get(self, request):
				user = users.get_current_user()
				...
	"""
	def check_login(self, request, *args):
		user = users.get_current_user()

		if not user:
			login_url = users.create_login_url(request.get_full_path())
			return HttpResponsePermanentRedirect(login_url)
		else:
			return handler_method(self, request, *args)

	return check_login
