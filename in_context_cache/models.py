from google.appengine.ext import ndb


class MyModel(ndb.Model):
	name = ndb.StringProperty()
