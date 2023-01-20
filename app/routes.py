from app import app
from flask import render_template

#routing for the application
@app.route('/')
def index():
	app.config['CURSOR'].execute("SELECT * FROM content_license")
	data = []
	for (id) in app.config['CURSOR']:
		data.append(id)
	return render_template('index.html', data=data)

@app.route('/dash')
def dashboard():
	return render_template('dash.html')