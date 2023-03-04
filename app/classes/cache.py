from redis import Redis
import json
class cache:
	def __init__(self, redis):
		self.redis = redis

	def cache_check(self,function):
		if(self.redis.exists(function)):
			cache_res = json.loads(self.redis.get(function))
		else:
			cache_res = False
		return cache_res
	
	def cache_set(self,function,data):
		try:
			self.redis.set(function, json.dumps(data))
			status = True
		except:
			status = False
		return status
