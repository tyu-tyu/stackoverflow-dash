import mariadb
from app.classes.cache import cache
import re
import os
from datetime import datetime
class lookup:
	def __init__(self, cursor, redis):
		self.cursor = cursor
		self.cache = cache(redis)

	def error_log(self, error):
		file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'error_log.txt'))
		with open(file_path, 'a') as error_log_file:
			error_log_file.write(str(datetime.now().strftime("%H:%M:%S"))+str(error)+'\n')

	def process_tag_form(self, form):
		data = form.to_dict()
		tag_list = []
		for key, value in data.items():
			if key == 'date_start':
				if re.match('^[\d]{4}-[\d]{2}-[\d]{2}$',value):
					date_start = value
				else:
					date_start = None
			elif key == 'date_end':
				if re.match('^[\d]{4}-[\d]{2}-[\d]{2}$',value):
					date_end = value
				else:
					date_end = None
			else:
				if re.match('^[0-9]+$',value):
					tag_list.append(value)
		if not tag_list:
			tag_list = ''
		else:
			tag_list = ','.join(tag_list)
		return (date_start,date_end,tag_list)

	def get_index_date_range(self):
		response = {}
		response['data'] = []
		cache = self.cache.cache_check('get_index_date_range')
		if cache == False:
			try:
				self.cursor.callproc('get_index_date_range')
				result = self.cursor.fetchall()
				for res in result:
					response['data'].append(res[0])
				self.cache.cache_set('get_index_date_range',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)
	
	def get_table_row_count(self):
		response = {}
		response['data'] = {}
		cache = self.cache.cache_check('get_table_row_count')
		if cache == False:
			try:
				self.cursor.callproc('get_table_row_count')
				result = self.cursor.fetchall()
				for res in result:
					response['data'][res[0]] = res[1]
				response['data']['posts'] = response['data']['question'] + response['data']['answer']
				self.cache.cache_set('get_table_row_count',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)
	
	def get_filtered_question_count(self, form):
		response = {}
		response['data'] = {}
		args = self.process_tag_form(form)
		try:
			self.cursor.callproc('get_filtered_question_count',args)
			result = self.cursor.fetchall()
			for res in result:
				response['data']['question'] = res[0]
			response['success'] = True
		except mariadb.Error as e:
			response['error'] = e
			response['success'] = False
			self.error_log(e)
		return(response)
	
	def get_top_tags(self,limit):
		response = {}
		response['data'] = {}
		response['data']['names'] = []
		response['data']['count'] = []
		cache = self.cache.cache_check('get_top_tags')
		if cache == False or len(cache['names']) != limit:
			try:
				self.cursor.callproc('get_top_tags',[limit,])
				result = self.cursor.fetchall()
				for res in result:
					response['data']['names'].append(res[0])
					response['data']['count'].append(res[1])
				self.cache.cache_set('get_top_tags',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)
	
	def get_top_badges(self,limit):
		response = {}
		response['data'] = {}
		response['data']['names'] = []
		response['data']['count'] = []
		cache = self.cache.cache_check('get_top_badges')
		if cache == False or len(cache['names']) != limit:
			try:
				self.cursor.callproc('get_top_badges',[limit,])
				result = self.cursor.fetchall()
				for res in result:
					response['data']['names'].append(res[0])
					response['data']['count'].append(res[1])
				self.cache.cache_set('get_top_badges',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)

	def get_index_question_details(self):
		response = {}
		response['data'] = []
		cache = self.cache.cache_check('get_index_question_details')
		if cache == False:
			try:
				self.cursor.callproc('get_index_question_details')
				result = self.cursor.fetchall()
				for res in result:
					response['data'].append(res[0])
				self.cache.cache_set('get_index_question_details',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)
	
	def get_filtered_question_details(self, form):
		args = self.process_tag_form(form)
		response = {}
		response['data'] = []
		try:
			self.cursor.callproc('get_filtered_question_details',args)
			result = self.cursor.fetchall()
			for res in result:
				response['data'].append(res[0])
			response['success'] = True
		except mariadb.Error as e:
			response['error'] = e
			response['success'] = False
			self.error_log(e)
		return(response)
	
	def get_user_years(self, form = None):
		response = {}
		response['data'] = {}
		response['data']['years'] = []
		response['data']['count'] = []
		if form != None:
			args = self.process_tag_form(form)
			cache = False
		else:
			cache = self.cache.cache_check('get_user_years')
			args = (None,None,'')
		if cache == False:
			try:
				self.cursor.callproc('get_user_years',args)
				result = self.cursor.fetchall()
				for res in result:
					response['data']['years'].append(res[0])
					response['data']['count'].append(res[1])
				response['success'] = True
				if form == None:
					self.cache.cache_set('get_user_years',response['data'])
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)
	
	def get_tag_list(self):
		response = {}
		response['data'] = []
		cache = self.cache.cache_check('get_tag_list')
		if cache == False:
			try:
				self.cursor.callproc('get_tag_list')
				result = self.cursor.fetchall()
				for res in result:
					row = {}
					row['id'] = res[0]
					row['tag'] = res[1]
					response['data'].append(row)
				self.cache.cache_set('get_tag_list',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)
	
	def get_filtered_tags(self, form = None):
		response = {}
		response['data'] = {}
		response['data']['tag_name'] = []
		response['data']['question_count'] = []
		response['data']['answer_count'] = []
		response['data']['comment_count'] = []
		response['data']['score'] = []
		response['data']['view_count'] = []
		response['data']['sentiment'] = []
		response['data']['link'] = []
		if form != None:
			args = self.process_tag_form(form)
			cache = False
		else:
			cache = self.cache.cache_check('get_filtered_tags')
			args = (None,None,'')
		if cache == False:
			try:
				self.cursor.callproc('get_filtered_tags',args)
				result = self.cursor.fetchall()
				for res in result:
					response['data']['tag_name'].append(res[0])
					response['data']['question_count'].append(res[1])
					response['data']['answer_count'].append(res[2])
					response['data']['comment_count'].append(res[3])
					response['data']['score'].append(res[4])
					response['data']['view_count'].append(res[5])
					response['data']['sentiment'].append(res[6])
					response['data']['link'].append(res[7])
				response['success'] = True
				if form == None:
					self.cache.cache_set('get_filtered_tags',response['data'])
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
			return(response)
		else:
			response['data'] = cache
		return(response)
	
	def get_post_keywords(self, form = None):
		response = {}
		response['data'] = {}
		response['data']['keyword'] = []
		response['data']['question_count'] = []
		response['data']['answer_count'] = []
		response['data']['comments_count'] = []
		response['data']['view_count'] = []
		response['data']['total_score'] = []
		response['data']['sentiment'] = []
		if form != None:
			args = self.process_tag_form(form)
			cache = False
		else:
			cache = self.cache.cache_check('get_post_keywords')
			args = (None,None,'')
		if cache == False:
			try:
				self.cursor.callproc('get_post_keywords',args)
				result = self.cursor.fetchall()
				for res in result:
					response['data']['keyword'].append(res[0])
					response['data']['question_count'].append(res[1])
					response['data']['answer_count'].append(res[2])
					response['data']['comments_count'].append(res[3])
					response['data']['view_count'].append(res[4])
					response['data']['total_score'].append(res[5])
					response['data']['sentiment'].append(res[6])
				if form == None:
					self.cache.cache_set('get_post_keywords',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)
	
	def get_top_posts(self, form = None):
		response = {}
		response['data'] = {}
		response['data']['title'] = []
		response['data']['score'] = []
		response['data']['link'] = []
		if form != None:
			args = self.process_tag_form(form)
			cache = False
		else:
			args = (None,None,'')
			cache = self.cache.cache_check('get_top_posts')
		if cache == False:
			try:
				self.cursor.callproc('get_top_posts',args)
				result = self.cursor.fetchall()
				for res in result:
					response['data']['title'].append(res[0])
					response['data']['score'].append(res[1])
					response['data']['link'].append(res[2])
				if form == None:
					self.cache.cache_set('get_top_posts',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)

	def get_user_keywords(self, form = None):
		response = {}
		response['data'] = {}
		response['data']['keyword'] = []
		response['data']['occ_count'] = []
		response['data']['avg_rep'] = []
		response['data']['total_rep'] = []
		response['data']['avg_acc_age'] = []
		if form != None:
			args = self.process_tag_form(form)
			cache = False
		else:
			args = (None,None,'')
			cache = self.cache.cache_check('get_user_keywords')
		if cache == False:
			try:
				self.cursor.callproc('get_user_keywords',args)
				result = self.cursor.fetchall()
				for res in result:
					response['data']['keyword'].append(res[0])
					response['data']['occ_count'].append(res[1])
					response['data']['avg_rep'].append(res[2])
					response['data']['total_rep'].append(res[3])
					response['data']['avg_acc_age'].append(res[4])
				if form == None:
					self.cache.cache_set('get_user_keywords',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
				self.error_log(e)
		else:
			response['data'] = cache
		return(response)
	
	def get_location_scores(self, form = None):
		response = {}
		response['data'] = {}
		response['data']['location'] = []
		response['data']['count'] = []
		response['data']['avg_rep'] = []
		response['data']['total_rep'] = []
		response['data']['question_count'] = []
		response['data']['answer_count'] = []
		response['data']['comment_count'] = []
		response['data']['avg_acc_age'] = []
		if form != None:
			args = self.process_tag_form(form)
			cache = False
		else:
			args = (None,None,'')
			cache = self.cache.cache_check('get_location_scores')
		if cache == False:
			try:
				self.cursor.callproc('get_location_scores',args)
				result = self.cursor.fetchall()
				for res in result:
					response['data']['location'].append(res[0])
					response['data']['count'].append(res[1])
					response['data']['avg_rep'].append(res[2])
					response['data']['total_rep'].append(res[3])
					response['data']['question_count'].append(res[4])
					response['data']['answer_count'].append(res[5])
					response['data']['comment_count'].append(res[6])
					response['data']['avg_acc_age'].append(res[7])
				if form == None:
					self.cache.cache_set('get_location_scores',response['data'])
				response['success'] = True
			except mariadb.Error as e:
				response['error'] = e
				response['success'] = False
		else:
			response['data'] = cache
		return(response)

	def get_filtered_top_badges(self, form):
		response = {}
		response['data'] = {}
		response['data']['names'] = []
		response['data']['count'] = []
		args = self.process_tag_form(form)
		try:
			self.cursor.callproc('get_filtered_top_badges',args)
			result = self.cursor.fetchall()
			for res in result:
				response['data']['names'].append(res[0])
				response['data']['count'].append(res[1])
			response['success'] = True
		except mariadb.Error as e:
			response['error'] = e
			response['success'] = False
			self.error_log(e)
		return(response)