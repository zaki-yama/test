# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from oauth2client.appengine import CredentialsNDBProperty

class CredentialsModel(ndb.Model):
	credentials = CredentialsNDBProperty()
