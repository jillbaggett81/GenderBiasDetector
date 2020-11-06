import os
from flask import Flask, request
from flask.templating import render_template
import logging

app = Flask(__name__, template_folder='templates')
print("logh")
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/<name>')
def hello_name(name):
    return "Hey {}!".format(name)

@app.route('/process_letter_text', methods=["GET","POST"])
def processLetter():
    text = request.form.get("letterText")
    return text + " this has been modified"

if __name__ == '__main__':
    app.run(debug=True)
