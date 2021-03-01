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
from flask_restful import Api, Resource
from flask.json import jsonify
import json

#initialize the class to process text
pc = ProcessText()
at = anonText()

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # new
db = SQLAlchemy(app)
ma = Marshmallow(app) 
api = Api(app)
logging.basicConfig(level=logging.DEBUG)

class Rec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #1 if male, 0 if female
    gender = db.Column(db.Integer)
    content = db.Column(db.String(500))

    def __repr__(self):
        return '<Review %s>' % self.content
class RecSchema(ma.Schema):
    class Meta:
        fields = ("id","gender","content")
        model = Rec
#Create Schema for our DB model
rec_schema = RecSchema()
recs_schema = RecSchema(many=True)

class PostListResource(Resource):
    def get(self):
        posts = Rec.query.all()
        return recs_schema.dump(posts)
    def post(self):
        new_post = Rec(
            gender=request.json['gender'],
            content=request.json['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return rec_schema.dump(new_post)
    def patch(self, post_id):
        post = Rec.query.get_or_404(post_id)

        if 'gender' in request.json:
            post.title = request.json['gender']
        if 'content' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return rec_schema.dump(post)

    def delete(self, post_id):
        post = Rec.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

class PostResource(Resource):
    def get(self, post_id):
        post = Rec.query.get_or_404(post_id)
        return rec_schema.dump(post)

api.add_resource(PostResource, '/posts/<int:post_id>')
api.add_resource(PostListResource, '/posts')
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

    #Post this to the DB

    to_post = Rec( gender = 0, content = text)
    db.session.add(to_post)
    db.session.commit()
    return render_template('text_analysis.html', results = result.json)

#We can eventually have this represent the results of machine learning for different words.
#This also could represent different ML models
#Src: https://rahmanfadhil.com/flask-rest-api/ 


if __name__ == '__main__':
    app.run(debug=True)
