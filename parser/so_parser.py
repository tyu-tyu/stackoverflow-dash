#Dependencies
import re
import xml.etree.ElementTree as et
from datetime import datetime
import os
import mariadb
import sys
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yake
#Pathing Variables
question_filename = os.path.join(os.path.dirname(__file__), 'output/question_import.csv')
answer_filename = os.path.join(os.path.dirname(__file__), 'output/answer_import.csv')
comments_filename = os.path.join(os.path.dirname(__file__), 'output/comments_import.csv')
user_filename = os.path.join(os.path.dirname(__file__), 'output/user_import.csv')
tag_filename = os.path.join(os.path.dirname(__file__), 'output/tag_import.csv')
taglist_filename = os.path.join(os.path.dirname(__file__), 'output/taglist_import.csv')
badgelist_filename = os.path.join(os.path.dirname(__file__), 'output/badgelist_import.csv')
keyword_filename = os.path.join(os.path.dirname(__file__), 'output/keyword_import.csv')
data_path = os.path.join(os.path.dirname(__file__), "data/")
os.makedirs(os.path.join(os.path.dirname(__file__), "output/"), exist_ok=True)
error_log_path = os.path.join(os.path.dirname(__file__), 'output/error_log.csv')
custom_kw_extractor = yake.KeywordExtractor(lan="en", n=1, dedupLim=0.9, top=5, features=None)

#Runs sql command based on whats called to it
def sql_import(type,cur,conn):
	if type == 'taglist':
		try:
			print("Importing Tags Please be patient")
			cur.execute("LOAD DATA LOCAL INFILE '"+tag_filename.replace('\\','/')+"' REPLACE INTO TABLE tag FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `tag`)")
			print("Done~")
		except mariadb.Error as e:
			log_error(e)
	elif type == 'taglink':
		try:
			print("Importing Tag links Please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_tag_link (id BIGINT, post_id BIGINT, tag_name VARCHAR(256));")
			cur.execute("LOAD DATA LOCAL INFILE '"+taglist_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_tag_link FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `post_id`, `tag_name`)")
			cur.execute("UPDATE temp_tag_link tl INNER JOIN tag AS t ON tl.tag_name = t.tag SET tl.`tag_name` = t.`id` WHERE tl.`tag_name` = t.`tag`;")
			cur.execute("INSERT INTO tag_link (post_id,tag_id) SELECT post_id, tag_name FROM temp_tag_link WHERE `tag_name` REGEXP '^[0-9]+$';")
			cur.execute("DROP TABLE temp_tag_link;")
			print("Done~")
		except mariadb.Error as e:
			log_error(e)
	elif type == 'question':
		try:
			print("Importing questions Please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_question like question;")
			cur.execute("LOAD DATA LOCAL INFILE '"+question_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_question FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `creation_date`, `score`, `view_count`, `title`, `sentiment`, `user_id`, `accepted_answer_id`)")
			cur.execute("INSERT IGNORE INTO question SELECT * FROM temp_question;")
			cur.execute("INSERT INTO `user` (id) SELECT user_id FROM temp_question WHERE user_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;")
			cur.execute("DROP TABLE temp_question;")
			print("Done~")
		except mariadb.Error as e:
			log_error(e)
	elif type == 'answer':
		try:
			print("Importing answers Please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_answer LIKE answer;")
			cur.execute("LOAD DATA LOCAL INFILE '"+answer_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_answer FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `question_id`, `creation_date`, `score`, `sentiment`,`user_id`);")
			cur.execute("INSERT IGNORE INTO answer SELECT * FROM temp_answer WHERE EXISTS (SELECT * FROM `question` where `id` = `question_id` LIMIT 1);")
			cur.execute("INSERT INTO `user` (id) SELECT user_id FROM temp_answer WHERE user_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;")
			cur.execute("DROP TABLE temp_answer;")
			print("Done~")
		except mariadb.Error as e:
			log_error(e)
	elif type == 'comments':
		try:
			print("Importing Comments Please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_comments LIKE comments;")
			cur.execute("LOAD DATA LOCAL INFILE '"+comments_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_comments FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `post_id`, `score`, `sentiment`,`creation_date`, `user_id`);")
			cur.execute("INSERT INTO comments SELECT * FROM temp_comments as tc WHERE EXISTS (SELECT * FROM question WHERE tc.`post_id` = question.`id` LIMIT 1) OR EXISTS (SELECT * FROM answer WHERE tc.`post_id` = answer.`id` LIMIT 1);")
			cur.execute("INSERT INTO `user` (id) SELECT user_id FROM temp_comments WHERE user_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;")
			cur.execute("DROP TABLE temp_comments;")
			print("Done~")
		except mariadb.Error as e:
			log_error(e)
	elif type == 'users':
		try:
			print("Importing users please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_user LIKE user;")
			cur.execute("LOAD DATA LOCAL INFILE '"+user_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_user FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `reputation`, `creation_date`, `location`);")
			cur.execute("UPDATE user AS u, temp_user AS tu SET u.reputation = tu.reputation, u.creation_date = tu.creation_date, u.location = tu.location WHERE u.id = tu.id;")
			cur.execute("DROP TABLE temp_user;")
			print("Done~")
		except mariadb.Error as e:
			log_error(e)
			conn.commit()
	elif type == 'badges':
		try:
			print("Importing badges please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_badge_link (`user_id` BIGINT, `badge` VARCHAR(256), `date` DATE);")
			cur.execute("LOAD DATA LOCAL INFILE '"+badgelist_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_badge_link FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`user_id`, `badge`, `date`);")
			cur.execute("DELETE FROM temp_badge_link WHERE NOT EXISTS (SELECT * FROM user u WHERE u.id = temp_badge_link.user_id);")
			cur.execute("ALTER TABLE `badge_link` CHANGE COLUMN `badge_id` `badge_id` VARCHAR(256) NOT NULL DEFAULT '0' AFTER `user_id`;")
			cur.execute("INSERT INTO badge_link (user_id, badge_id, date) SELECT * FROM temp_badge_link;")
			cur.execute("DROP TABLE temp_badge_link;")
			print("Done~")
		except mariadb.Error as e:
			log_error(e)
	elif type == 'keyword':
		try:
			print("Importing keywords please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_keyword_link (`post_id` BIGINT, `comment_id` BIGINT, `user_id` BIGINT, `keyword_id` VARCHAR(256));")
			cur.execute("LOAD DATA LOCAL INFILE '"+keyword_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_keyword_link CHARACTER SET UTF8 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`post_id`, `comment_id`, `user_id`, `keyword_id`);")
			cur.execute("INSERT INTO keyword_link (post_id,comment_id,user_id,keyword_id) SELECT * FROM temp_keyword_link;")
			cur.execute("DROP TABLE temp_keyword_link;")
			print("Done~")
		except mariadb.Error as e:
			log_error(e)
	conn.commit()
#Works out sentiment score
def sentiment_scores(text):
	sid_obj = SentimentIntensityAnalyzer()
	sentiment = sid_obj.polarity_scores(text)
	sentiment_score = sentiment['compound']*100
	return sentiment_score

def keywords(k_writer,text,type,id):
	keywords=custom_kw_extractor.extract_keywords(text)
	for kw in keywords:
		if type == 'post':
			cols = [id,'\\N','\\N',re.sub('(,)|(\\n)|(\\\\)','', kw[0][:255])]
		elif type == 'comments':
			cols = ['\\N',id,'\\N',re.sub('(,)|(\\n)|(\\\\)','', kw[0][:255])]
		elif type == 'user':
			cols = ['\\N','\\N',id,re.sub('(,)|(\\n)|(\\\\)','', kw[0][:255])]

		k_writer.writerow(cols)

def log_error(error):
	with open(error_log_path, "a") as elwr:
		elwr.write(str(error))
		elwr.close()

if __name__ == "__main__":
	# Connect to MariaDB Platform
	try:
		conn = mariadb.connect(
			user="root",
			password="username",
			host="localhost",
			port=5505,
			database="password",
			local_infile = 1
		)
	except mariadb.Error as e:
		print(f"Error connecting to MariaDB Platform: {e}")
		sys.exit(1)
	cur = conn.cursor()

	#Get a valid date from user to parse from
	valid = False
	while valid == False:
		date_start = input("Please enter the START date you wish to parse from (YYYY-MM-DD) >")
		if re.match('([0-9]{4}-[0-9]{2}-[0-9]{2})',date_start):
			date_end = input("Please enter the END date you wish to parse from (YYYY-MM-DD) >")
			if re.match('([0-9]{4}-[0-9]{2}-[0-9]{2})',date_end):
				try:
					date_start = datetime.strptime(date_start, '%Y-%m-%d')
					date_end = datetime.strptime(date_end, '%Y-%m-%d')
				except:
					print('ERROR: Invalid Date entered')
				if date_start > date_end:
					print('ERROR: End Date cannot be newer than Start Date')
				else:
					row_limit = input("Optional: Would you like a limit on total number of questions processed? > ")
					if re.match('[0-9]+',row_limit):
						row_limit = int(row_limit)
						use_row_limit = True
					else:
						use_row_limit = False
					valid = True

	#counter variable
	row_count = 0

	# ---------------------------------------------------------------------------- #
	#                                     Tags                                     #
	# ---------------------------------------------------------------------------- #
	with open(data_path+"Tags.xml", encoding="utf-8") as source, open(tag_filename, 'a', newline='', encoding='utf-8') as twr:
		t_writer = csv.writer(twr, delimiter=',')
		context = et.iterparse(source, events=("start", "end"))
		for index, (event, elem) in enumerate(context):
			# Get the root element.
			if index == 0:
				root = elem
			if event == "end" and elem.tag == "row":
				if 'TagName' in elem.attrib and elem.attrib['TagName'] != "":
					tagname = re.sub('(,)|(\\n)|(\\\\)','', elem.attrib['TagName'])
					cols = [elem.attrib['Id'],tagname]
					if tagname != '':
						t_writer.writerow(cols)
				root.clear()
		sql_import('taglist',cur,conn)
	source.close()
	twr.close()
	# # ---------------------------------------------------------------------------- #
	# #                                     Posts                                    #
	# # ---------------------------------------------------------------------------- #
	with open(keyword_filename, 'a', newline='', encoding='utf-8') as kwr:
		k_writer = csv.writer(kwr, delimiter=',')
		with open(data_path+"Posts.xml", encoding="utf-8") as source, open(question_filename, 'a', newline='', encoding='utf-8') as qwr, open(answer_filename, 'a', newline='', encoding='utf-8') as awr, open(taglist_filename, 'a', newline='', encoding='utf-8') as tlwr:
			q_writer = csv.writer(qwr, delimiter=',')
			a_writer = csv.writer(awr, delimiter=',')
			tl_writer = csv.writer(tlwr, delimiter=',')
			# Get an iterable.
			context = et.iterparse(source, events=("start", "end"))
			for index, (event, elem) in enumerate(context):
				# Get the root element.
				if index == 0:
					root = elem
				if event == "end" and elem.tag == "row":
					if (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') >= date_start) and (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') <= date_end):
						if int(elem.attrib['PostTypeId']) == 1:
							#checking optional xml columns and processing
							if 'Body' in elem.attrib and elem.attrib['Body'] != "":
								keywords(k_writer,elem.attrib['Body'],'post',elem.attrib['Id'])
								sent_score = sentiment_scores(elem.attrib['Body'])
							else:
								body = '\\N'
								sent_score = '\\N'
							if 'OwnerUserId' in elem.attrib:
								user_id = elem.attrib['OwnerUserId']
							else:
								user_id = '\\N'
							if 'AcceptedAnswerId' in elem.attrib:
								accepted_reply_id = elem.attrib['AcceptedAnswerId']
							else:
								accepted_reply_id = '\\N'
							if 'Tags' in elem.attrib:
								#Insert tags + taglinks into DB
								tags = elem.attrib['Tags'].split('>')
								for tag in tags:
									tag = re.sub('(<)|(,)', '', tag)
									cols = ['\\N',elem.attrib['Id'], tag]
									if tag:
										tl_writer.writerow(cols)
							#defines question columns and adds to csv
							cols = [
								elem.attrib['Id'],
								elem.attrib['CreationDate'][0:10],
								elem.attrib['Score'],
								elem.attrib['ViewCount'],
								re.sub('(,)|(\\n)|(\\\\)', '', elem.attrib['Title']),
								sent_score,
								user_id,
								accepted_reply_id
							]
							q_writer.writerow(cols)
							row_count = row_count+1
						elif int(elem.attrib['PostTypeId']) == 2: #Answer processing
							if 'OwnerUserId' in elem.attrib:
								user_id = elem.attrib['OwnerUserId']
							else:
								user_id = '\\N'
							keywords(k_writer,elem.attrib['Body'],'post',elem.attrib['Id'])
							#defines columns to add to the answer
							cols = [
								elem.attrib['Id'],
								elem.attrib['ParentId'],
								elem.attrib['CreationDate'][0:10],
								elem.attrib['Score'],
								sentiment_scores(elem.attrib['Body']),
								user_id
							]
							a_writer.writerow(cols)
					elif datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') > date_end:
						break
					root.clear()
				if (use_row_limit == True) and (row_count >= row_limit):
					break
		#Adding final posts to DB that aren't done during the staged import
		sql_import('taglink',cur,conn)
		sql_import('question',cur,conn)
		sql_import('answer',cur,conn)
		source.close()
		qwr.close()
		awr.close()
		tlwr.close()

		# ---------------------------------------------------------------------------- #
		#                                   Comments                                   #
		# ---------------------------------------------------------------------------- #

		with open(data_path+"Comments.xml", encoding="utf-8") as source, open(comments_filename, 'a', newline='', encoding='utf-8') as cwr:
			c_writer = csv.writer(cwr, delimiter=',')
		# Get an iterable.
			context = et.iterparse(source, events=("start", "end"))
			for index, (event, elem) in enumerate(context):
				# Get the root element.
				if index == 0:
					root = elem
				if event == "end" and elem.tag == "row":
					if (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') >= date_start) and (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') <= date_end):
						if 'UserId' in elem.attrib:
							user_id = elem.attrib['UserId']
						else:
							user_id = '\\N'
						keywords(k_writer,elem.attrib['Text'],'comments',elem.attrib['Id'])
						cols = [
							elem.attrib['Id'],
							elem.attrib['PostId'],
							elem.attrib['Score'],
							sentiment_scores(elem.attrib['Text']),
							elem.attrib['CreationDate'][0:10],
							user_id
						]
						c_writer.writerow(cols)
					if datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') > date_end:
						break
				root.clear()
			source.close()
		#Adding final posts to DB
		sql_import('comments',cur,conn)
		source.close()
		cwr.close()
		# ---------------------------------------------------------------------------- #
		#                                     Users                                    #
		# ---------------------------------------------------------------------------- #
		cur.execute("SELECT id FROM user ORDER BY id ASC")
		user_list = []
		result = cur.fetchall()
		for res in result:
			user_list.append(res[0])

		with open(data_path+"Users.xml", encoding="utf-8") as source, open(user_filename, 'a', newline='', encoding='utf-8') as uwr:
			u_writer = csv.writer(uwr, delimiter=',')
		# Get an iterable.
			context = et.iterparse(source, events=("start", "end"))
			for index, (event, elem) in enumerate(context):
				# Get the root element.
				if index == 0:
					root = elem
				if event == "end" and elem.tag == "row":
					if datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') <= date_end:
							if int(elem.attrib['Id']) in user_list:
								if 'Location' in elem.attrib and elem.attrib['Location'] != "":
									location = re.sub('(,)|(\\n)|(\\\\)','', elem.attrib['Location'])
								else:
									location = '\\N'
								if 'AboutMe' in elem.attrib and elem.attrib['AboutMe'] != "":
									keywords(k_writer,elem.attrib['AboutMe'],'user',elem.attrib['Id'])
								cols = [elem.attrib['Id'],elem.attrib['Reputation'],elem.attrib['CreationDate'][0:10],location]
								u_writer.writerow(cols)
								user_list.remove(int(elem.attrib['Id']))
					if (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') > date_end) and (int(elem.attrib['Id']) > 0):
						break
					root.clear()
			source.close()
		sql_import('users',cur,conn)
		source.close()
		uwr.close()
	kwr.close()
	sql_import('keyword',cur,conn)
	# ---------------------------------------------------------------------------- #
	#                                    Badges                                    #
	# ---------------------------------------------------------------------------- #
	with open(data_path+"Badges.xml", encoding="utf-8") as source, open(badgelist_filename, 'a', newline='', encoding='utf-8') as blwr:
		bl_writer = csv.writer(blwr, delimiter=',')
		# Get an iterable.
		context = et.iterparse(source, events=("start", "end"))
		for index, (event, elem) in enumerate(context):
			# Get the root element.
			if index == 0:
				root = elem
			if event == "end" and elem.tag == "row":
				if (datetime.strptime(elem.attrib['Date'][0:10], '%Y-%m-%d') >= date_start) and (datetime.strptime(elem.attrib['Date'][0:10], '%Y-%m-%d') <= date_end):
					cols  = [elem.attrib['UserId'],elem.attrib['Name'],elem.attrib['Date'][0:10]]
					bl_writer.writerow(cols)
				if datetime.strptime(elem.attrib['Date'][0:10], '%Y-%m-%d') > date_end:
					break
			root.clear()
		source.close()
		blwr.close()
	sql_import('badges',cur,conn)
 	#Normalize the badges
	cur.execute("INSERT INTO badges (`badge_name`) SELECT DISTINCT `badge_id` FROM badge_link;")
	cur.execute("UPDATE badge_link bl INNER JOIN badges AS b ON bl.badge_id = b.badge_name SET bl.`badge_id` = b.`id`;")
	conn.commit()
	#Normalize the keywords
	cur.execute("INSERT INTO keyword (`keyword`) SELECT DISTINCT `keyword_id` FROM keyword_link;")
	cur.execute("UPDATE keyword_link kl INNER JOIN keyword as k ON kl.keyword_id = k.keyword SET kl.`keyword_id` = k.`id`")
	conn.commit()
