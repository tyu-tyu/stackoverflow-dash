import mariadb
class home_page:
	def __init__(self, cursor):
		self.cursor = cursor

	def get_content_license(self):
		response = {}
		response["data"] = []
		try:
			self.cursor.execute("SELECT `content_license` FROM content_license")
			result = self.cursor.fetchall()
			for res in result:
				response["data"].append(res[0])
			response["status"] = True
		except mariadb.Error as e:
			response["data"].append(e)
			response["success"] = False
		return(response)
	
	def get_question_range(self):
		response = {}
		response["data"] = []
		try:
			self.cursor.callproc("get_question_date_range")
			result = self.cursor.fetchall()
			for res in result:
				response["data"].append(res[0])
			response["status"] = True
		except mariadb.Error as e:
			response["data"].append(e)
			response["success"] = False
		return(response)