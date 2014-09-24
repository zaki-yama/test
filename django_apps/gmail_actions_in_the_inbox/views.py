# -*- coding: utf-8 -*-
import logging
from urlparse import urlparse

from google.appengine.api import mail
from google.appengine.api import users

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect
from django.template import Context, loader
from django.views.generic.base import View


logger = logging.getLogger(__name__)


class EmailSenderView(View):

	def get(self, request):
		# require users to be logged in to send emails
		user = users.get_current_user()
		if not user:
			return redirect(users.create_login_url(request.path))

		email = user.email()
		logger.warn(request.path)

		# the review url corresponds to the App Engine app url
		pr = urlparse(request.build_absolute_uri())
		app_name = request.resolver_match.app_name
		review_url = '%s://%s/' % (pr.scheme, pr.netloc)

		# load the email template and replace the placeholder with the review url
		template = loader.get_template('mail_template.html')
		template_values = {
				'review_url': review_url,
				}
		email_body = loader.render_to_string('mail_template.html', Context(template_values))

		message = mail.EmailMessage(
				sender=email,
				to=email,
				subject='Please review Google Cafe',
				html=email_body)

		try:
			message.send()
			return HttpResponse('OK')
		except:
			return HttpResponseServerError()
