# Stack Overflow Dashboard project
A project for parsing + displaying custom metrics from the Stack Overflow data dump: https://archive.org/details/stackexchange on the web
## Installation

Installation can be made easy using Docker simply download the project, pick a schema either the empty one or if you have a schema with preparsed data and rename it to `schema.sql` this is the file MariaDB will build the database from when built in Docker.
run the following commands:
  - docker-compose build
  - docker-compose up
  
Your project will now be running, to view the database login using one of the following methods:
  - mariadb client locally (HeidiSQL)
    - Hostname: 127.0.0.1
    - user: username
    - password: password
    - port: 5505
  - PHPMyAdmin
    - url: http://localhost:800/ by default
    - user: username
    - password: password
	
	(these can be edited in the docker-compose file)
### Parsing your data
*full disclaimer python xml parsing is line by line and very slow, forking for speed welcome*
1. Download the following files from the Stack Exchange dump: https://archive.org/details/stackexchange
	- stackoverflow.com-Badges.7z
	- stackoverflow.com-Comments.7z
	- stackoverflow.com-Posts.7z
	- stackoverflow.com-Tags.7z
	- stackoverflow.com-Users.7z
2. Unzip the XML and put it in a folder at the following path: `Your-link-to-project/parser/data`
3. pip install the following requirements (The parser is unable to be dockerized as Docker cannot handle importing XMLs of this size reliably):
	- mariadb
	- vaderSentiment
	- yake
4. Run the parser, setting a date you wish to parse between and an optional limit\
  *How much should I parse?* Depends on your hardware a month of data is roughly:
	 - 150,000 Questioins 
	 - 110,00 Answers 
	 - 350,000 Comments
	 - 180,000 Users	
5. Go to sleep or something this will take a while
### Viewing the app
- head over to http://localhost:4996/ by default
- Filter results on any of the pages if you wish
- Export the data for any future usage

### Maintanence
To reset the redis cache if a new dataset is to be imported or any errors occur the easiest way is the following:
 - open your docker gui and click on the redis container
 - open the terminal of that redis container
 - type in `redis-cli` 
 - type in `flushdb`
 - this should return a one once flushed, if not try again you can check with the `keys *` command

This app has logging found in the error_log.txt for any SQL or connection errors
