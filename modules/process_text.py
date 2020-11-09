from flask import Flask, current_app, jsonify
from flask.templating import render_template
import logging
import os
from functools import wraps
import urllib.parse
import string


#Eventually we can epand this class to pull to and from the db as needed.
#This way we can better segment and manipulate our information

#Communal affectionate, helpful, kind, sympathetic,



class ProcessText():
    def __init__(self):
        self.config = None
    def process_text(self,data):
        result = self.process_without_ML(data)
        return(result)
    def process_without_ML(self,data):
        agentic_terms = []
        communal_terms = ['sympathetic','kind','help','affection','sensitive','nurtur','agreeab','tactful','interpersonal','warm','car','tactful']
        socio_communal = []
        #This splits the input text on white spaces
        
        words_no_punc = data.translate(str.maketrans('', '', string.punctuation))
        words = data.split()
        agentic = 0
        communal = 0
        socio_comm = 0
        for i in words:
            for j in agentic_terms:
                if j in i.lower():
                    agentic += 1
            for j in communal_terms:
                if j in i.lower():
                    communal += 1
            for j in socio_communal:
                if j in i.lower():
                    socio_communal += 1
        return jsonify({"agentic":agentic, "communal":communal, "socio_communal":socio_comm})
