#Dependencies
import re
import xml.etree.ElementTree as et
from datetime import datetime
import csv
import os
#row processed counter
count = 0
#used to grab from other files
tag_list = []
post_list = []
user_list = []
comment_list = []
badge_list = []
#incremental filenames to help with insert
question_filecount = 1
taglink_filecount = 1
answer_filecount = 1
user_filecount = 1
comment_filecount = 1
badgelink_filecount = 1
#Pathing variables
os.makedirs(os.path.join(os.path.dirname(__file__), "output/"), exist_ok=True)
data_path = os.path.join(os.path.dirname(__file__), "data/")

#printing to csv function
def output_csv(filename,columns):
	with open(filename, 'a', newline='', encoding='utf-8') as wr:
		writer = csv.writer(wr, delimiter=',')
		writer.writerow(columns)
		wr.close()

#checking if file is ~250MB increments output filename if so
def increment_file(filename,count):
	if os.path.getsize(filename) > 262140000:
		count = count+1
	return count

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
				if(int(elem.attrib['PostTypeId']) == 1):
					#checking optional xml columns and processing
					if 'Body' in elem.attrib and elem.attrib['Body'] != "":
						body = re.sub(',', '', elem.attrib['Body'])
					else:
						body = 'NULL'
					if elem.attrib["ContentLicense"] == 'CC BY-SA 2.5':
						content_license = 1
					elif elem.attrib["ContentLicense"] == 'CC BY-SA 3.0':
						content_license = 2
					else:
						content_license = 3
					if 'LastEditDate' in elem.attrib:
						edit_date = elem.attrib['LastEditDate'][0:10]
					else:
						edit_date = 'NULL'
					activity_date = elem.attrib['LastActivityDate'][0:10]
					if 'OwnerUserId' in elem.attrib:
						user_id = elem.attrib['OwnerUserId']
						if user_id not in user_list:
								user_list.append(user_id)
					else:
						user_id = 'NULL'
					if 'LastEditorUserId' in elem.attrib:
						editor_id = elem.attrib['LastEditorUserId']
						if user_id not in user_list:
							user_list.append(user_id)
					else:
						editor_id = 'NULL'
					if 'AcceptedAnswerId' in elem.attrib:
						accepted_reply_id = elem.attrib['AcceptedAnswerId']
					else:
						accepted_reply_id = 'NULL'
					if 'Tags' in elem.attrib:
						tags = elem.attrib['Tags'].split('>') #Split tags from csv in data
						for tag in tags:
							#Adds tag to list if not present
							tag = re.sub('<', '', tag)
							if tag not in tag_list:
								tag_list.append(tag)
							tag_links = [elem.attrib['Id'],tag_list.index(tag)] #Adds post_id and tag_id from the array into the list
							#Adds the necessary data to the taglink import file
							taglink_filename = os.path.join(os.path.dirname(__file__), "output/taglink_import"+str(taglink_filecount)+'.csv')
							output_csv(taglink_filename,tag_links)
							taglink_filecount = increment_file(taglink_filename,taglink_filecount)
					#Outputs the data to the question import csv
					question_columns = [elem.attrib['Id'],elem.attrib['CreationDate'][0:10],elem.attrib['Score'],elem.attrib['ViewCount'],body,re.sub(',', '', elem.attrib['Title']),content_license,edit_date,activity_date,user_id,editor_id,accepted_reply_id]
					question_filename = os.path.join(os.path.dirname(__file__), "output/question_import"+str(question_filecount)+'.csv')
					output_csv(question_filename,question_columns)
					question_filecount = increment_file(question_filename,question_filecount)
					post_list.append(elem.attrib['Id'])
				elif(int(elem.attrib['PostTypeId']) == 2): #Answer processing
					if elem.attrib['ParentId'] in post_list:
						if elem.attrib["ContentLicense"] == 'CC BY-SA 2.5':
							content_license = 1
						elif elem.attrib["ContentLicense"] == 'CC BY-SA 3.0':
							content_license = 2
						else:
							content_license = 3
						if 'LastEditDate' in elem.attrib:
							edit_date = elem.attrib['LastEditDate'][0:10]
						else:
							edit_date = 'NULL'
						activity_date = elem.attrib['LastActivityDate'][0:10]
						if 'OwnerUserId' in elem.attrib:
							user_id = elem.attrib['OwnerUserId']
							if user_id not in user_list:
								user_list.append(user_id)
						else:
							user_id = 'NULL'
						if 'LastEditorUserId' in elem.attrib:
							editor_id = elem.attrib['LastEditorUserId']
							if user_id not in user_list:
								user_list.append(user_id)
						else:
							editor_id = 'NULL'
						#defines columns to add to the answer
						answer_columns = [elem.attrib['Id'],elem.attrib['ParentId'],elem.attrib['CreationDate'][0:10],elem.attrib['Score'],re.sub(',', '', elem.attrib['Body']),user_id,editor_id,edit_date,activity_date,content_license]
						answer_filename = os.path.join(os.path.dirname(__file__), "output/answer_import"+str(answer_filecount)+'.csv')
						output_csv(answer_filename,answer_columns)
						answer_filecount = increment_file(answer_filename,answer_filecount)
						post_list.append(elem.attrib['Id'])
			elif datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') >= date_end:
				source.close()
				break
			print("Processing Posts Id:",elem.attrib['Id'],"Created",elem.attrib['CreationDate'][0:10])
			root.clear()
		if (use_row_limit == True) and (len(post_list) >= row_limit):
			source.close()
			break
	source.close()
# ---------------------------------------------------------------------------- #
#                                    TagList                                   #
# ---------------------------------------------------------------------------- #
taglist_filename = os.path.join(os.path.dirname(__file__), "output/tag_import.csv")
output_csv(taglist_filename,tag_list)
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
				if (elem.attrib['PostId'] in(post_list)):
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
							user_id = 'NULL'
					comments_columns = [elem.attrib['Id'],elem.attrib['PostId'],elem.attrib['Score'],re.sub(',', '', elem.attrib['Text']),elem.attrib['CreationDate'][0:10],user_id,content_license]
					comments_filename = os.path.join(os.path.dirname(__file__), "output/comment_import"+str(comment_filecount)+'.csv')
					output_csv(comments_filename,comments_columns)
					comment_filecount = increment_file(comments_filename,comment_filecount)
			print("Processing Comments:",elem.attrib['Id'],"Created",elem.attrib['CreationDate'][0:10])
		root.clear()
	source.close()
# Post List can be unset to save memory as it is no longer needed
post_list = []
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
			if (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') >= date_start) and (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') <= date_end):
				if(int(elem.attrib['Id']) in(user_list)):
					users_columns = [elem.attrib['Id'],elem.attrib['Reputation'],elem.attrib['CreationDate'][0:10],re.sub(',', '', elem.attrib['Location'])]
					users_filename = os.path.join(os.path.dirname(__file__), "output/user_import"+str(user_filecount)+'.csv')
					output_csv(users_filename,users_columns)
					user_filecount = increment_file(users_filename,user_filecount)
			print("Processing Users Id:",elem.attrib['Id'],"Created",elem.attrib['CreationDate'][0:10])
	source.close()
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
			if (datetime.strptime(elem.attrib['Date'][0:10], '%Y-%m-%d') >= date_start) and (datetime.strptime(elem.attrib['CreationDate'][0:10], '%Y-%m-%d') <= date_end):
				if(int(elem.attrib['UserId']) in(user_list)):
					if elem.attrib['Name'] not in badge_list:
						badge_list.append(elem.attrib['Name'])
					badge_links = [elem.attrib['UserId'],badge_list.index(elem.attrib['Name'])] #Adds post_id and tag_id from the array into the list
					#Adds the necessary data to the taglink import file
					badgelink_filename = os.path.join(os.path.dirname(__file__), "output/badgelink_import"+str(badgelink_filecount)+'.csv')
					output_csv(badgelink_filename,badge_links)
					badgelink_filecount = increment_file(badgelink_filename,badgelink_filecount)
			print("Processing Badges Id:",elem.attrib['Id'])
		root.clear()
	source.close()
user_list = []
#importing badge to the tag lookup table
badgelist_filename = os.path.join(os.path.dirname(__file__), "output/badge_import.csv")
output_csv(badgelist_filename,badge_list)

#Beep to let you know the application 2has finished parsing sucessfully
print('===Parsing Complete===')
print('\a')