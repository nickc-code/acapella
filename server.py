from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)


@app.route('/')
def Home():
	return render_template('Home.html')






if __name__ == '__main__':
	app.run()
