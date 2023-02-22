from app import app
from flask import render_template
#routing for the application
@app.route('/')
def index():
	from app.lookups.home_page import home_page
	result_data = {}
	lookups = home_page(app.config['CURSOR'])
	result_data["content_licenses"] = lookups.get_content_license()
	result_data["question_date_range"] = lookups.get_index_date_range()
	result_data["table_row_count"] = lookups.get_table_row_count()
	result_data["top_10_tags"] = lookups.get_top_10_tags()
	return render_template('index.html.jinja', data=result_data)

@app.route('/trending')
def trending():
	return render_template('trending.html.jinja')
