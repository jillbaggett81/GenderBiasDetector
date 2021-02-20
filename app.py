import os
import sys
from sys import path
path.append('./modules')
from flask import Flask, request, current_app
from flask.templating import render_template
import logging
import modules
from modules.process_text import ProcessText
from modules.anonymizeText import anonText
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask.json import jsonify
import json

#initialize the class to process text
pc = ProcessText()
at = anonText()

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # new
db = SQLAlchemy(app)
ma = Marshmallow(app) 
logging.basicConfig(level=logging.DEBUG)

#Home page for Flask
#Run this application using "python3 app.py" then go to localhost:5000 on Chrome
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/process_letter_text', methods=["GET","POST"])
def processLetter():
    current_app.logger.info(request.form)
    if "anonymize" in request.form.get("action"):
            text = request.form.get("letterText")
            student_name = request.form.get("studentName")
            result = at.anonymize(text, student_name)
            current_app.logger.info(result)
            return result
        
       #Extract user text from the form
    text = request.form.get("letterText")
    #Send the text to the processing module 
    result = pc.process_text(text)
    print(result)
    #Return results of the processing module in a new page
    current_app.logger.info(result.json['communal'])
    return render_template('text_analysis.html', results = result.json)

#We can eventually have this represent the results of machine learning for different words.
#This also could represent different ML models
#Src: https://rahmanfadhil.com/flask-rest-api/ 
class Word(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    weight = db.Column(db.Integer)
    content = db.Column(db.Integer)

    def __repr__(self):
        return '<Word %s>' % self.id
class WordSchema(ma.Schema):
    class Meta:
        fields = ("id", "weight", "content")
        model = Word
#Create Schema for our DB model
word_schema = WordSchema()
words_schema = WordSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
