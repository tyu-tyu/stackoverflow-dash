#windows registry mimetype fix
import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index(name=None):
	return render_template('index.html', name=name)

@app.route('/dash')
def dashboard():
	return render_template('dash.html')

if __name__ == '__main__':
	app.run(debug=True,port=4996)