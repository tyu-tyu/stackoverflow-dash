from app import app
from flask import render_template
import mariadb
db_config = {
	'user':'root',
	'password':'tyudb99',
	'host':'127.0.0.1',
	'port':3306,
	'database': 'dashboard_data'
}
conn = mariadb.connect(**db_config)
cur = conn.cursor()

@app.route('/')
def index(name=None):
	cur.execute("SELECT * FROM content_license")
	data = []
	for (id) in cur:
		data.append(id)
	return render_template('index.html', name=name, data=data)

@app.route('/dash')
def dashboard():
	return render_template('dash.html')