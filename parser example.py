import re
import xml.etree.ElementTree as et
import datetime
import csv
count = 0
now = datetime.datetime.now()
with open('Posts.xml', encoding='utf8') as f:
	for line in f:
		try:
			tree = et.fromstring(line)
			last_activity_date = datetime.datetime.strptime(tree.attrib['LastActivityDate'][0:10], '%Y-%m-%d')
			days = (now - last_activity_date).days
			if int(tree.attrib['PostTypeId']) == 1 and days <= 1095:
				question_id = tree.attrib['Id']
				creation_date = tree.attrib['CreationDate'][0:10]
				score = tree.attrib['Score']
				view_count = tree.attrib['ViewCount']
				body = re.sub(',', '', tree.attrib['Body']) 
				title = re.sub(',', '', tree.attrib['Title'])
				if tree.attrib["ContentLicense"] == 'CC BY-SA 2.5':
					content_license = 1
				elif tree.attrib["ContentLicense"] == 'CC BY-SA 3.0':
					content_license = 2
				else:
					content_license = 3
				if 'LastEditDate' in tree.attrib:
					edit_date = tree.attrib['LastEditDate'][0:10]
				else:
					edit_date = 'NULL'
				activity_date = tree.attrib['LastActivityDate'][0:10]
				if 'OwnerUserId' in tree.attrib:
					user_id = tree.attrib['OwnerUserId']
				else:
					user_id = 'NULL'
				if 'LastEditorUserId' in tree.attrib:
					editor_id = tree.attrib['LastEditorUserId']
				else:
					editor_id = 'NULL'
				if 'AcceptedAnswerId' in tree.attrib:
					accepted_reply_id = tree.attrib['AcceptedAnswerId']
				else:
					accepted_reply_id = 'NULL'
				script = [question_id,creation_date,score,view_count,body,title,content_license,edit_date,activity_date,user_id,editor_id,accepted_reply_id]
				print(script)
				with open("insert_file.csv", "a", newline='') as y:
					csv.writer(y).writerow(script)
					y.close()
		except:
			with open("failed_lines.csv", "a", encoding="utf-8") as x:
				x.write(line)
				x.close()

		count = count + 1
		print("count:",count)