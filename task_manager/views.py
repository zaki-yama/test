# -*- coding: utf-8 -*-
import httplib2
import logging
import os
import settings

from google.appengine.api import users

from apiclient.discovery import build
from oauth2client import xsrfutil
from oauth2client.appengine import StorageByKeyName
from oauth2client.client import flow_from_clientsecrets

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .models import CredentialsModel
from utils.login import login_required


logger = logging.getLogger(__name__)

SCOPE = 'https://www.googleapis.com/auth/tasks'
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')
FLOW = flow_from_clientsecrets(
		CLIENT_SECRETS,
		scope=SCOPE,
		redirect_uri='http://localhost:8080/task_manager/oauth2callback')


class MainView(View):
	template_name = 'task_manager/index.html'

	@login_required
	def get(self, request):
		user = users.get_current_user()
		storage = StorageByKeyName(
				CredentialsModel, user.email(), 'credentials')
		# logger.info(type(storage))
		credentials = storage.get()
		# logger.info(type(credentials))
		if credentials is None or credentials.access_token_expired:
			FLOW.params['state'] = xsrfutil.generate_token(
					settings.SECRET_KEY, user)
			authorize_url = FLOW.step1_get_authorize_url()
			logging.info(authorize_url)
			return HttpResponseRedirect(authorize_url)
		else:
			http = httplib2.Http()
			http = credentials.authorize(http)
			service = build('tasks', 'v1', http=http)
			tasks = service.tasks().list(tasklist='@default').execute(http=http)
			template_values={
					'logout_url': users.create_logout_url(request.get_full_path()),
					'app_name':request.resolver_match.app_name,
					'tasks':tasks['items'],
					}
			template_values.update(csrf(request))
			return render(request, self.template_name, template_values)


class AuthView(View):

	def get(self, request):
		user = users.get_current_user()
		credentials = FLOW.step2_exchange(request.REQUEST)
		storage = StorageByKeyName(
				CredentialsModel, user.email(), 'credentials')
		storage.put(credentials)
		return HttpResponseRedirect('/task_manager')
