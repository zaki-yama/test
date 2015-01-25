# -*- coding: utf-8 -*-
import logging
import os

from google.appengine.api import users

from apiclient.discovery import build
from oauth2client.appengine import StorageByKeyName
from oauth2client.client import flow_from_clientsecrets

from django.http import HttpResponseRedirect
from django.views.generic.base import View

from .models import CredentialsModel


logger = logging.getLogger(__name__)

service = build('tasks', 'v1')

SCOPE = 'https://www.googleapis.com/auth/tasks'
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')
FLOW = flow_from_clientsecrets(
		CLIENT_SECRETS,
		scope=SCOPE,
		redirect_uri='http://localhost:8080/task_manager/oauth2callback')


class MainView(View):

	def get(self, request):
		if users.get_current_user():
			authorize_url = FLOW.step1_get_authorize_url()
			logger.info(authorize_url)
			return HttpResponseRedirect(authorize_url)
		else:
			login_url = users.create_login_url(request.get_full_path())
			return  HttpResponseRedirect(login_url)


class AuthView(View):

	def get(self, request):
		credentials = FLOW.step2_exchange(request.REQUEST)
		storage = StorageByKeyName(
				CredentialsModel, 'admin@example.com', 'credentials')
		storage.put(credentials)
		return HttpResponseRedirect('/')
