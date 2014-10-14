# -*- coding: utf-8 -*-
import os
import sys


def webapp_add_wsgi_middleware(app):
	from google.appengine.ext.appstats import recording
	app = recording.appstats_wsgi_middleware(app)
	return app


ROOTPATH = os.path.dirname(__file__)
LIBPATH = os.path.join(ROOTPATH, 'libs')
sys.path.append(LIBPATH)
