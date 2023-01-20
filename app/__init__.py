#dependencies for init
import mimetypes
import mariadb
from app.db_config import db_config
from flask import Flask

#mimetype fix to allow external html + css
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/html', '.html')

#initiate app class
app = Flask(__name__, static_folder='../static/')
from app import routes

#app database connections
app.config['DATABASE'] = mariadb.connect(**db_config())
app.config['CURSOR'] = app.config['DATABASE'].cursor()
