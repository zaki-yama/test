# -*- coding: utf-8 -*-
import logging
import os
import settings

from google.appengine.api import users
from google.appengine.ext import ndb

from apiclient.discovery import build
from oauth2client.appengine import OAuth2WebServerFlow, StorageByKeyName
from oauth2client.client import flow_from_clientsecrets

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from models import CredentialsModel

# ロガーインスタンスを取得
logger = logging.getLogger(__name__)

service = build('tasks', 'v1')


# FLOW = OAuth2WebServerFlow(
		# client_id=settings.CLIENT_ID,
		# client_secret=settings.CLIENT_SECRET,
		# redirect_uri='http://localhost:8080/task_manager/oauth2callback',
		# scope=settings.SCOPE,
		# user_agent='my-sample/1.0')
SCOPE = 'https://www.googleapis.com/auth/tasks'
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')
FLOW = flow_from_clientsecrets(
		CLIENT_SECRETS,
		scope=SCOPE,
		redirect_uri='http://localhost:8080/task_manager/oauth2callback')

# authorize_url = flow.step1_get_authorize_url()
# self.redirect(authorize_url)

# credentials = flow.step2_exchange(self.request.params)
# storage = StorageByKeyName(
		# Credentials, user.user_id(), 'credentials'
		# )
# storage.put(credentials)

# user = user.get_current_user()
# storage = StorageByKeyName(
		# Credentials, user.user_id(), 'credentials'
		# )
# credentials = storage.get()

# http = httplib2.Http()
# http = credentials.authorize(http)

class MainView(View):

	def get(self, request):
		if users.get_current_user():
			authorize_url = FLOW.step1_get_authorize_url()
			logger.info(authorize_url)
			return HttpResponseRedirect(authorize_url)
		else:
			login_url = users.create_login_url(request.get_full_path())
			return  HttpResponseRedirect(login_url)

	# @decorator.oauth_required
	# def get(self, request):
		# tasks = service.tasks().list(tasklist='@default').execute(
				# http=decorator.http())
		# template_values = {
				# 'app_name': request.resolver_match.app_name,
				# 'tasks': tasks['items'],
				# }
		# template_values.update(csrf(request))
		# return render(request, self.template_name, template_values)

	# @method_decorator(login_required)
	# def dispatch(self, *args, **kwargs):
		# return super(MainView, self).dispatch(*args, **kwargs)


class AuthView(View):

	def get(self, request):
		logger.warn('::::::::::::::::::::::::::::::::')
		# logger.warn(request.user)
		credentials = FLOW.step2_exchange(request.REQUEST)
		storage = StorageByKeyName(
				CredentialsModel, 'admin@zaki-yama.com', 'credentials')
		storage.put(credentials)
		return HttpResponseRedirect('/')
