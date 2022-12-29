from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=False,port=4996)