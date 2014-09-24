# -*- coding: utf-8 -*-
import logging
from urlparse import urlparse

from google.appengine.api import mail
from google.appengine.api import users

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render, redirect
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.decorators import method_decorator

from .models import Review


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
		review_url = '%s://%s/%s/' % (pr.scheme, pr.netloc, app_name)

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


class ReviewHandlerView(View):

	def get(self, request):
		# retrieve up to 1000 reviews from the Datastore
		reviews = Review.query().fetch(1000)

		if not reviews:
			return HttpResponse('No reviews')

		total = 0
		count = len(reviews)
		response = HttpResponse()

		for r in reviews:
			total += r.rating_value
			review_body = r.review_body or 'No feedback'
			response.write('%d/5 - %s<br />' % (r.rating_value, review_body))

		response.write('<br />')
		response.write('%d reviews - Average rating %.2f/5' % (count, total / float(count)))

		return response

	def post(self, request):
		rating_value = request.POST.get('review.reviewRating.ratingValue')
		review_body = request.POST.get('review.reviewBody')

		# the numeric rating is required
		if not rating_value:
			return HttpResponseBadRequest()

		# insert the review into the Datastore
		review = Review(rating_value=int(rating_value), review_body=review_body)
		review.put()

		return HttpResponse('OK')

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(ReviewHandlerView, self).dispatch(*args, **kwargs)
