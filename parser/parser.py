#Dependencies
import re
import xml.etree.ElementTree as et
from datetime import datetime
import os
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="tyu",
        password="tyudb99",
        host="localhost",
        port=5505,
        database="dashboard_data"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

if __name__ == "__main__":
	cur = conn.cursor()

	#Pathing variables
	data_path = os.path.join(os.path.dirname(__file__), "data/")

	user_list = []
	row_count = 0

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
					row_limit = input("Optional: Would you like a limit on total number of rows processed? > ")
					if re.match('[0-9]+',row_limit):
						row_limit = int(row_limit)
						use_row_limit = True
					else:
						use_row_limit = False
					valid = True
	# ---------------------------------------------------------------------------- #
	#                                     Posts                                    #
	# ---------------------------------------------------------------------------- #
	with open(data_path+"Posts.xml", encoding="utf-8") as source:
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
							body = elem.attrib['Body']
						else:
							body = None
						if elem.attrib["ContentLicense"] == 'CC BY-SA 2.5':
							content_license = 1
						elif elem.attrib["ContentLicense"] == 'CC BY-SA 3.0':
							content_license = 2
						else:
							content_license = 3
						if 'LastEditDate' in elem.attrib:
							edit_date = elem.attrib['LastEditDate'][0:10]
						else:
							edit_date = None
						activity_date = elem.attrib['LastActivityDate'][0:10]
						if 'OwnerUserId' in elem.attrib:
							user_id = elem.attrib['OwnerUserId']
							if user_id not in user_list:
								user_list.append(user_id)
						else:
							user_id = None
						if 'LastEditorUserId' in elem.attrib:
							editor_id = elem.attrib['LastEditorUserId']
							if editor_id not in user_list:
								user_list.append(editor_id)
						else:
							editor_id = None
						if 'AcceptedAnswerId' in elem.attrib:
							accepted_reply_id = elem.attrib['AcceptedAnswerId']
						else:
							accepted_reply_id = None
						if 'Tags' in elem.attrib:
							tags = elem.attrib['Tags'].split('>')
							for tag in tags:
								tag = re.sub('(<)|(,)', '', tag)
								#Insert tags + taglinks into DB
								cur.callproc(
									'insert_taglink',
									(elem.attrib['Id'], tag)
								)
						#Insert Questions into DB
						cur.callproc(
							'insert_question',
							(elem.attrib['Id'],elem.attrib['CreationDate'][0:10],elem.attrib['Score'],elem.attrib['ViewCount'],body,elem.attrib['Title'],content_license,edit_date,activity_date,user_id,editor_id,accepted_reply_id)
						)
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
							edit_date = None
						activity_date = elem.attrib['LastActivityDate'][0:10]
						if 'OwnerUserId' in elem.attrib:
							user_id = elem.attrib['OwnerUserId']
							if user_id not in user_list:
								user_list.append(user_id)
						else:
							user_id = None
						if 'LastEditorUserId' in elem.attrib:
							editor_id = elem.attrib['LastEditorUserId']
							if editor_id not in user_list:
								user_list.append(user_id)
						else:
							editor_id = None
						#defines columns to add to the answer
						cur.callproc(
							'insert_answer',
							(elem.attrib['Id'],elem.attrib['ParentId'],elem.attrib['CreationDate'][0:10],elem.attrib['Score'],elem.attrib['Body'],user_id,editor_id,edit_date,activity_date,content_license)
						)
					row_count = row_count+1
				elif datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') > date_end:
					break
				print('Processing Post id: ', elem.attrib['Id'],"Date: ",elem.attrib['CreationDate'])
				root.clear()
			if (use_row_limit == True) and (row_count >= row_limit):
				break
		source.close()
	conn.commit()
	# ---------------------------------------------------------------------------- #
	#                                   Comments                                   #
	# ---------------------------------------------------------------------------- #
	with open(data_path+"Comments.xml", encoding="utf-8") as source:
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
						if user_id not in user_list:
							user_list.append(user_id)
						else:
							user_id = None
					cur.callproc(
						'insert_comment',
						(elem.attrib['Id'],elem.attrib['PostId'],elem.attrib['Score'],elem.attrib['Text'],elem.attrib['CreationDate'][0:10],user_id,content_license)
					)
				print("Processing Comments:",elem.attrib['Id'],"Created: ",elem.attrib['CreationDate'])
				if datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') > date_end:
					break
			root.clear()
		source.close()
	conn.commit()
	# ---------------------------------------------------------------------------- #
	#                                     Users                                    #
	# ---------------------------------------------------------------------------- #
	with open(data_path+"Users.xml", encoding="utf-8") as source:
	# Get an iterable.
		context = et.iterparse(source, events=("start", "end")) 
		for index, (event, elem) in enumerate(context):
			# Get the root element.
			if index == 0:
				root = elem
			if event == "end" and elem.tag == "row":
				if datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') <= date_end:
					if elem.attrib['Id'] in(user_list):
						if 'Location' in elem.attrib:
							location = elem.attrib['Location']
						else:
							location = None
						cur.callproc(
							'insert_user',
							(elem.attrib['Id'],elem.attrib['Reputation'],elem.attrib['CreationDate'][0:10],location)
						)
				print("Processing Users Id:",elem.attrib['Id'],"Created",elem.attrib['CreationDate'])
				if (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') > date_end) and (int(elem.attrib['Id']) > 0):
					break
				root.clear()
		source.close()
	conn.commit()
	# ---------------------------------------------------------------------------- #
	#                                    Badges                                    #
	# ---------------------------------------------------------------------------- #
	with open(data_path+"Badges.xml", encoding="utf-8") as source:
	# Get an iterable.
		context = et.iterparse(source, events=("start", "end")) 
		for index, (event, elem) in enumerate(context):
			# Get the root element.
			if index == 0:
				root = elem
			if event == "end" and elem.tag == "row":
				if (datetime.strptime(elem.attrib['Date'][0:10], '%Y-%m-%d') >= date_start) and (datetime.strptime(elem.attrib['Date'][0:10], '%Y-%m-%d') <= date_end):
					if elem.attrib['UserId'] in(user_list):
						cur.callproc(
							'insert_badges',
							(elem.attrib['UserId'],elem.attrib['Name'],elem.attrib['Date'][0:10])
						)
				print("Processing Badges Id:",elem.attrib['Id'],"Created",elem.attrib['Date'])
				if datetime.strptime(elem.attrib['Date'][0:10], '%Y-%m-%d') > date_end:
					break
			root.clear()
		source.close()
	conn.commit()