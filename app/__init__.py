#windows registry mimetype fix
import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/html', '.html')

from flask import Flask
app = Flask(__name__, static_folder='../static/')
from app import routes

app.run(
	debug=True,
	port=4996
)

