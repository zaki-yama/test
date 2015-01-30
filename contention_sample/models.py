from google.appengine.ext import ndb

import logging

logger = logging.getLogger(name='hoge')

class MyModel(ndb.Model):
	name = ndb.StringProperty(indexed=False)

	@classmethod
	def upsert_multi(cls, num):
		logger.info(num)
		return [future.get_result() for future in cls.upsert_multi_async(num)]

	@classmethod
	def upsert_multi_async(cls, num, **kwargs):
		return [cls.upsert_async() for i in xrange(num)]

	@classmethod
	@ndb.tasklet
	def upsert_async(cls):

		@ndb.tasklet
		def txn():
			logger.info('txn')
			key = ndb.Key(cls, 'hoge')
			obj = yield key.get_async()

			if not obj:
				obj = cls(key=key)
			yield obj.put_async()

			logger.info('call get_parent_async')
			parent = yield obj.get_parent_async()
			parent.content = 'hogehoge'
			logger.info('put parent')
			yield parent.put_async()

			raise ndb.Return(obj)

		res = yield ndb.transaction_async(txn, xg=True)
		raise ndb.Return(res)

	def get_parent(self):
		return self.get_parent_async().get_result()

	@ndb.tasklet
	def get_parent_async(self):
		logger.info('get_parent_async')
		key = ndb.Key(MyModel, 'fuga')
		parent = yield key.get_async()
		if not parent:
			parent = MyModel(key=key)
		raise ndb.Return(parent)

