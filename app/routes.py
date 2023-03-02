from app import app
from flask import render_template, request
#routing for the application
@app.route('/')
def index():
	from app.lookups.home_page import home_page
	result_data = {}
	lookups = home_page(app.config['CURSOR'])
	result_data['content_licenses'] = lookups.get_content_license()
	result_data['question_date_range'] = lookups.get_index_date_range()
	result_data['table_row_count'] = lookups.get_table_row_count()
	result_data['top_tags'] = lookups.get_top_tags(10)
	result_data['top_badges'] = lookups.get_top_badges(10)
	result_data['question_details'] = lookups.get_index_question_details()
	return render_template('index.html.jinja', data=result_data)

@app.route('/trending')
def trending():
	return render_template('trending.html.jinja')

@app.route('/ajax/update_index_tag_chart')
def update_index_tag_chart():
	from app.lookups.home_page import home_page
	lookups = home_page(app.config['CURSOR'])
	result_data = lookups.get_top_tags(request.args.get('count'))
	return result_data

@app.route('/ajax/update_index_badge_chart')
def update_index_badge_chart():
	from app.lookups.home_page import home_page
	lookups = home_page(app.config['CURSOR'])
	result_data = lookups.get_top_badges(request.args.get('count'))
	return result_data