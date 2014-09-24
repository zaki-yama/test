# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class Review(ndb.Model):
	rating_value = ndb.IntegerProperty(required=True)
	review_body = ndb.TextProperty(required=False)
