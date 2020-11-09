import os
import sys
from sys import path
path.append('./modules')
from flask import Flask, request, current_app
from flask.templating import render_template
import logging
import modules
from modules.process_text import ProcessText

#initialize the class to process text
pc = ProcessText()

app = Flask(__name__, template_folder='templates')
logging.basicConfig(level=logging.DEBUG)

#Home page for Flask
#Run this application using "python3 app.py" then go to localhost:5000 on Chrome
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/process_letter_text', methods=["GET","POST"])
def processLetter():

    #Extract user text from the form
    text = request.form.get("letterText")

    #Send the text to the processing module 
    result = pc.process_text(text)

    #Return results of the processing module in a new page
    current_app.logger.info(result.json['communal'])
    return render_template('text_analysis.html', results = result)

if __name__ == '__main__':
    app.run(debug=True)
