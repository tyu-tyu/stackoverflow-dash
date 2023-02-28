#Dependencies
import re
import xml.etree.ElementTree as et
from datetime import datetime
import os
import mariadb
import sys
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Pathing Variables 
question_filename = os.path.join(os.path.dirname(__file__), 'output/question_import.csv')
answer_filename = os.path.join(os.path.dirname(__file__), 'output/answer_import.csv')
comments_filename = os.path.join(os.path.dirname(__file__), 'output/comments_import.csv')
user_filename = os.path.join(os.path.dirname(__file__), 'output/user_import.csv')
tag_filename = os.path.join(os.path.dirname(__file__), 'output/tag_import.csv')
taglist_filename = os.path.join(os.path.dirname(__file__), 'output/taglist_import.csv')
badgelist_filename = os.path.join(os.path.dirname(__file__), 'output/badgelist_import.csv')
data_path = os.path.join(os.path.dirname(__file__), "data/")
os.makedirs(os.path.join(os.path.dirname(__file__), "output/"), exist_ok=True)

#Runs sql command based on whats called to it
def sql_import(type,cur,conn):
	if type == 'taglist':
		try:
			print("importing Tags Please be patient")
			cur.execute("LOAD DATA LOCAL INFILE '"+tag_filename.replace('\\','/')+"' REPLACE INTO TABLE tag FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `tag`)")
			conn.commit()
		except mariadb.Error as e:
			print(f"Error: {e}")
	elif type == 'taglink':
		try:
			print("importing Tag links Please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_tag_link (id BIGINT, post_id BIGINT, tag_name VARCHAR(256));")
			cur.execute("LOAD DATA LOCAL INFILE '"+taglist_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_tag_link FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `post_id`, `tag_name`)")
			cur.execute("UPDATE temp_tag_link tl INNER JOIN tag AS t ON tl.tag_name = t.tag SET tl.`tag_name` = t.`id` WHERE tl.`tag_name` = t.`tag`;")
			cur.execute("INSERT INTO tag_link (post_id,tag_id) SELECT post_id, tag_name FROM temp_tag_link WHERE `tag_name` REGEXP '^[0-9]+$';")
			cur.execute("DROP TABLE temp_tag_link;")
			conn.commit()
		except mariadb.Error as e:
			print(f"Error: {e}")
	elif type == 'question':
		try:
			print("Importing questions Please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_question like question;")
			cur.execute("LOAD DATA LOCAL INFILE '"+question_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_question FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `creation_date`, `score`, `view_count`, `body`, `title`, `sentiment`,`content_license`, `edit_date`, `activity_date`, `user_id`, `editor_id`, `accepted_answer_id`)")
			cur.execute("INSERT INTO question SELECT * FROM temp_question;")
			cur.execute("INSERT INTO `user` (id) SELECT user_id FROM temp_question WHERE user_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;")
			cur.execute("INSERT INTO `user` (id) SELECT editor_id FROM temp_question WHERE editor_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;")
			cur.execute("DROP TABLE temp_question;")
			conn.commit()
		except mariadb.Error as e:
			print(f"Error: {e}")
	elif type == 'answer':
		try:
			print("Importing answers Please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_answer LIKE answer;")
			cur.execute("LOAD DATA LOCAL INFILE '"+answer_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_answer FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `question_id`, `creation_date`, `score`, `body`, `sentiment`,`user_id`, `editor_id`, `edit_date`, `activity_date`, `content_license`);")
			cur.execute("INSERT INTO answer SELECT * FROM temp_answer WHERE EXISTS (SELECT * FROM `question` where `id` = `question_id` LIMIT 1);")
			cur.execute("INSERT INTO `user` (id) SELECT user_id FROM temp_answer WHERE user_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;")
			cur.execute("INSERT INTO `user` (id) SELECT editor_id FROM temp_answer WHERE editor_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;")
			cur.execute("DROP TABLE temp_answer;")
			conn.commit()
		except mariadb.Error as e:
			print(f"Error: {e}")
	elif type == 'comments':
		try:
			print("Importing Comments Please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_comments LIKE comments;")
			cur.execute("LOAD DATA LOCAL INFILE '"+comments_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_comments FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `post_id`, `score`, `text`, `sentiment`,`creation_date`, `user_id`, `content_license`);")
			cur.execute("INSERT INTO comments SELECT * FROM temp_comments as tc WHERE EXISTS (SELECT * FROM question WHERE tc.`post_id` = question.`id` LIMIT 1) OR EXISTS (SELECT * FROM answer WHERE tc.`post_id` = answer.`id` LIMIT 1);")
			cur.execute("INSERT INTO `user` (id) SELECT user_id FROM temp_comments WHERE user_id <> 'NULL' ON DUPLICATE KEY UPDATE user.id=user.id;")
			cur.execute("DROP TABLE temp_comments;")
			conn.commit()
		except mariadb.Error as e:
			print(f"Error: {e}")
	elif type == 'users':
		try:
			print("Importing users please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_user LIKE user;")
			cur.execute("LOAD DATA LOCAL INFILE '"+user_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_user FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`id`, `reputation`, `creation_date`, `location`, `about_me`);")
			cur.execute("UPDATE user AS u, temp_user AS tu SET u.reputation = tu.reputation, u.creation_date = tu.creation_date, u.location = tu.location, u.about_me = tu.about_me WHERE u.id = tu.id;")
			cur.execute("DROP TABLE temp_user;")
			conn.commit()
		except mariadb.Error as e:
			print(f"Error: {e}")
			cur.execute("DROP TABLE temp_user;")
			conn.commit()
	elif type == 'badges':
		try:
			print("Importing badges please be patient")
			cur.execute("CREATE TEMPORARY TABLE temp_badge_link (`user_id` BIGINT, `badge` VARCHAR(256), `date` DATE);")
			cur.execute("LOAD DATA LOCAL INFILE '"+badgelist_filename.replace('\\','/')+"' REPLACE INTO TABLE temp_badge_link FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' (`user_id`, `badge`, `date`);")
			cur.execute("DELETE FROM temp_badge_link WHERE NOT EXISTS (SELECT * FROM user u WHERE u.id = temp_badge_link.user_id);")
			cur.execute("INSERT INTO badge_link (user_id, badge_id, date) SELECT * FROM temp_badge_link;")
			cur.execute("DROP TABLE temp_badge_link;")
			conn.commit()
		except mariadb.Error as e:
			print(f"Error: {e}")

#Works out sentiment score
def sentiment_scores(text):
	sid_obj = SentimentIntensityAnalyzer()
	sentiment = sid_obj.polarity_scores(text)
	sentiment_score = sentiment['compound']*100
	return sentiment_score

if __name__ == "__main__":
	# Connect to MariaDB Platform
	try:
		conn = mariadb.connect(
			user="tyu",
			password="tyudb99",
			host="localhost",
			port=5505,
			database="dashboard_data",
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
		cur.execute("TRUNCATE TABLE tag")
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
				print('Processing Tag id: ', elem.attrib['Id'])
				root.clear()
		sql_import('taglist',cur,conn)
		twr.truncate(0)
		source.close()
		twr.close()
	# ---------------------------------------------------------------------------- #
	#                                     Posts                                    #
	# ---------------------------------------------------------------------------- #

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
							body = re.sub('(,)|(\\n)|(\\\\)','', elem.attrib['Body'])
							sent_score = sentiment_scores(body)
						else:
							body = '\\N'
							sent_score = '\\N'
						if elem.attrib["ContentLicense"] == 'CC BY-SA 2.5':
							content_license = 1
						elif elem.attrib["ContentLicense"] == 'CC BY-SA 3.0':
							content_license = 2
						else:
							content_license = 3
						if 'LastEditDate' in elem.attrib:
							edit_date = elem.attrib['LastEditDate'][0:10]
						else:
							edit_date = '\\N'
						activity_date = elem.attrib['LastActivityDate'][0:10]
						if 'OwnerUserId' in elem.attrib:
							user_id = elem.attrib['OwnerUserId']
						else:
							user_id = '\\N'
						if 'LastEditorUserId' in elem.attrib:
							editor_id = elem.attrib['LastEditorUserId']
						else:
							editor_id = '\\N'
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
								if os.path.getsize(taglist_filename) > 50000000:
									sql_import('taglink',cur,conn)
									tlwr.truncate(0)
						#defines question columns and adds to csv
						cols = [
							elem.attrib['Id'],
							elem.attrib['CreationDate'][0:10],
							elem.attrib['Score'],
							elem.attrib['ViewCount'],
							body,
							re.sub('(,)|(\\n)|(\\\\)', '', elem.attrib['Title']),
							sent_score,
							content_license,
							edit_date,
							activity_date,
							user_id,
							editor_id,
							accepted_reply_id
						]
						q_writer.writerow(cols)
						if os.path.getsize(question_filename) > 50000000:
							sql_import('question',cur,conn)
							qwr.truncate(0)
						row_count = row_count+1
					elif int(elem.attrib['PostTypeId']) == 2: #Answer processing
						if elem.attrib["ContentLicense"] == 'CC BY-SA 2.5':
							content_license = 1
						elif elem.attrib["ContentLicense"] == 'CC BY-SA 3.0':
							content_license = 2
						else:
							content_license = 3
						if 'LastEditDate' in elem.attrib:
							edit_date = elem.attrib['LastEditDate'][0:10]
						else:
							edit_date = '\\N'
						activity_date = elem.attrib['LastActivityDate'][0:10]
						if 'OwnerUserId' in elem.attrib:
							user_id = elem.attrib['OwnerUserId']
						else:
							user_id = '\\N'
						if 'LastEditorUserId' in elem.attrib:
							editor_id = elem.attrib['LastEditorUserId']
						else:
							editor_id = '\\N'
						#defines columns to add to the answer
						cols = [
							elem.attrib['Id'],
							elem.attrib['ParentId'],
							elem.attrib['CreationDate'][0:10],
							elem.attrib['Score'],
							re.sub('(,)|(\\n)','', elem.attrib['Body']),
							sentiment_scores(elem.attrib['Body']),
							user_id,
							editor_id,
							edit_date,
							activity_date,
							content_license
						]
						a_writer.writerow(cols)
						if os.path.getsize(answer_filename) > 50000000:
							sql_import('answer',cur,conn)
							awr.truncate(0)
				elif datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') > date_end:
					break
				print('Processing Post id: ', elem.attrib['Id'],"Date: ",elem.attrib['CreationDate'])
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
					if elem.attrib["ContentLicense"] == 'CC BY-SA 2.5':
						content_license = 1
					elif elem.attrib["ContentLicense"] == 'CC BY-SA 3.0':
						content_license = 2
					else:
						content_license = 3
					if 'UserId' in elem.attrib:
						user_id = elem.attrib['UserId']
					else:
						user_id = '\\N'		
					cols = [
						elem.attrib['Id'],
						elem.attrib['PostId'],
						elem.attrib['Score'],
						re.sub('(,)|(\\n)|(\\\\)','', elem.attrib['Text']),
						sentiment_scores(elem.attrib['Text']),
						elem.attrib['CreationDate'][0:10],
						user_id,
						content_license]
					c_writer.writerow(cols)
					if os.path.getsize(comments_filename) > 50000000:
						sql_import('comments',cur,conn)
						cwr.truncate(0)
				print("Processing Comments:",elem.attrib['Id'],"Created: ",elem.attrib['CreationDate'])
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
						if 'Location' in elem.attrib and elem.attrib['Location'] != "":
							location = re.sub('(,)|(\\n)|(\\\\)','', elem.attrib['Location'])
						else:
							location = '\\N'
						if 'AboutMe' in elem.attrib and elem.attrib['AboutMe'] != "":
							about_me = re.sub('(,)|(\\n)|(\\\\)','', elem.attrib['AboutMe'])
						else:
							about_me = '\\N'
						cols = [elem.attrib['Id'],elem.attrib['Reputation'],elem.attrib['CreationDate'][0:10],location,about_me]
						u_writer.writerow(cols)
						if os.path.getsize(user_filename) > 25000000:
							sql_import('users',cur,conn)
							uwr.truncate(0)
				print("Processing Users Id:",elem.attrib['Id'],"Created",elem.attrib['CreationDate'])
				if (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') > date_end) and (int(elem.attrib['Id']) > 0):
					break
				root.clear()
		source.close()
	sql_import('users',cur,conn)
	source.close()
	uwr.close()
	
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
					if os.path.getsize(badgelist_filename) > 50000000:
						sql_import('badges',cur,conn)
						blwr.truncate(0)
				print("Processing Badges Id:",elem.attrib['Id'],"Created",elem.attrib['Date'])
				if datetime.strptime(elem.attrib['Date'][0:10], '%Y-%m-%d') > date_end:
					break
			root.clear()
		source.close()
		blwr.close()
	sql_import('badges',cur,conn)
	#Inserts final badges into DB
	cur.execute("INSERT INTO badges (`badge_name`) SELECT DISTINCT `badge_id` FROM badge_link;")
	cur.execute("ALTER TABLE `badge_link` CHANGE COLUMN `badge_id` `badge_id` VARCHAR(256) NOT NULL DEFAULT '0' AFTER `user_id`;")
	cur.execute("UPDATE badge_link bl INNER JOIN badges AS b ON bl.badge_id = b.badge_name SET bl.`badge_id` = b.`id`;")
	cur.execute("ALTER TABLE `badge_link` CHANGE COLUMN `badge_id` `badge_id` BIGINT NOT NULL DEFAULT 0 COLLATE 'utf8mb3_general_ci' AFTER `user_id`;")
	conn.commit()
	#Cleaning up import files
	os.remove(question_filename)
	os.remove(answer_filename)
	os.remove(comments_filename )
	os.remove(user_filename)
	os.remove(tag_filename)
	os.remove(taglist_filename)
	os.remove(badgelist_filename)