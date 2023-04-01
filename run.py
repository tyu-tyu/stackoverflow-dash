#entry point for the app
from app import app

#running the app
app.run(
	debug=False,
	port=4996,
	host=('0.0.0.0')
)