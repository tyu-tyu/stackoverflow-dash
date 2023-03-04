from redis import Redis
class cache:
	def __init__(self, redis):
		self.redis = redis

	def cache_check(self,cache):
		return cache