# -*- encoding: utf-8 -*-
import urllib

from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.views.generic import View

from google.appengine.api import users

from .models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME


class MainView(View):
	template_name = 'guestbook/main_page.html'

	def get(self, request):
		guestbook_name = request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)

		# Ancestor Queries, as shown here, are strongly consistent with the High
		# Replication Datastore. Queries that span entity groups are eventually
		# consistent. If we omitted the ancestor from this query there would be
		# a slight chance that Greeting that had just been written would not
		# show up in a query.
		greetings_query = Greeting.query(
				ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = greetings_query.fetch(10)

		if users.get_current_user():
			url = users.create_logout_url(request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(request.get_full_path())
			url_linktext = 'Login'

		template_values = {
				# 'user':      user,
				'greetings': greetings,
				'guestbook_name': guestbook_name,
				'url': url,
				'url_linktext': url_linktext,
				}
		template_values.update(csrf(request))
		return render(request, self.template_name, template_values)


class PostView(View):

	def post(self, request):
		# We set the same parent key on the 'Greeting' to ensure each Greeting
		# is in the same entity group. Queries across the single entity group
		# will be consistent. However, the write rate to a single entity group
		# should be limited to ~1/second.
		guestbook_name = request.POST.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)

		greeting = Greeting(parent=guestbook_key(guestbook_name))

		if users.get_current_user():
			greeting.author = users.get_current_user()

		greeting.content = request.POST.get('content')
		greeting.put()

		query_params = {'guestbook_name': guestbook_name}
		return redirect('/?' + urllib.urlencode(query_params))
