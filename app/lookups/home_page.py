import mariadb
class home_page:
	def __init__(self, cursor):
		self.cursor = cursor

	def get_content_license(self):
		response = {}
		response['data'] = []
		try:
			self.cursor.execute('SELECT `content_license` FROM content_license')
			result = self.cursor.fetchall()
			for res in result:
				response['data'].append(res[0])
			response['status'] = True
		except mariadb.Error as e:
			response['data'].append(e)
			response['success'] = False
		return(response)
	
	def get_index_date_range(self):
		response = {}
		response['data'] = []
		try:
			self.cursor.callproc('get_index_date_range')
			result = self.cursor.fetchall()
			for res in result:
				response['data'].append(res[0])
			response['status'] = True
		except mariadb.Error as e:
			response['data'].append(e)
			response['success'] = False
		return(response)
	
	def get_table_row_count(self):
		response = {}
		response['data'] = {}
		try:
			self.cursor.callproc('get_table_row_count')
			result = self.cursor.fetchall()
			for res in result:
				response['data'][res[0]] = res[1]
			response['data']['posts'] = response['data']['question'] + response['data']['answer']
			response['status'] = True
		except mariadb.Error as e:
			response['data'].append(e)
			response['success'] = False
		return(response)
	
	def get_top_tags(self,limit):
		response = {}
		response['data'] = {}
		response['data']['names'] = []
		response['data']['count'] = []
		try:
			self.cursor.callproc('get_top_tags',[limit,])
			result = self.cursor.fetchall()
			for res in result:
				response['data']['names'].append(res[0])
				response['data']['count'].append(res[1])
			response['status'] = True
		except mariadb.Error as e:
			response['data'].append(e)
			response['success'] = False
		return(response)
	
	def get_top_badges(self,limit):
		response = {}
		response['data'] = {}
		response['data']['names'] = []
		response['data']['count'] = []
		try:
			self.cursor.callproc('get_top_badges',[limit,])
			result = self.cursor.fetchall()
			for res in result:
				response['data']['names'].append(res[0])
				response['data']['count'].append(res[1])
			response['status'] = True
		except mariadb.Error as e:
			response['data'].append(e)
			response['success'] = False
		return(response)

	def get_index_question_details(self):
		response = {}
		response['data'] = []
		try:
			self.cursor.callproc('get_index_question_details')
			result = self.cursor.fetchall()
			for res in result:
				response['data'].append(res[0])
			response['status'] = True
		except mariadb.Error as e:
			response['data'].append(e)
			response['success'] = False
		return(response)