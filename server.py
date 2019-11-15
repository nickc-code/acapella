from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)


@app.route('/')
def Home():
	return render_template('Home.html')

@app.route('/SingerHome')
def SingerHome():
	return render_template('SingerHome.html')

@app.route('/Soppranos')
def Soppranos():
	return render_template('Soppranos.html')






if __name__ == '__main__':
	app.run()
