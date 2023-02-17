from app import app
from flask import render_template
#routing for the application
@app.route('/')
def index():
	from app.lookups.home_page import home_page
	result_data = {}
	lookups = home_page(app.config['CURSOR'])
	result_data["content_licenses"] = lookups.get_content_license()
	result_data["question_date_range"] = lookups.get_question_range()
	return render_template('index.html', data=result_data)

@app.route('/dash')
def dashboard():
	return render_template('dash.html')