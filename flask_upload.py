import os
from PIL import Image
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_ngrok import run_with_ngrok

from werkzeug.utils import secure_filename

from model.quickdraw_test import show_inference

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/canvas")
def canvas():
	return render_template('canvas.html')

@app.route("/uploadFile/<path>", methods = ['POST'])
def upload_file(path):
	file = request.files['file']
	if path == 'file':
		if file.filename == '':
			return redirect(url_for('canvas'))
		else:
			file.save('drawing.png')
	elif path == 'canvas':
		img = Image.open(file.stream)
		img = img.resize((600, 600), Image.ANTIALIAS)
		img.save('drawing.png') # "draing.png" 파일이 저장됨
	return redirect(url_for('analyze'))

@app.route("/analyze")
def analyze(result=None):
	# show_inference(model, "drawing.png") #???????
	return render_template('result.html', result=result)

if __name__ == '__main__':
	app.run()