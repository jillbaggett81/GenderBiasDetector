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
        agentic_terms = ['assertive','confident','aggressive','ambitious','dominan','forceful','independent','daring','outspoken','intellectua','earn','gain','know','insight','think']
        communal_terms = ['sympathetic','kind','help','affection','sensitive','nurtur','agreeab','tactful','interpersonal','warm','car','tactful']
        socio_communal = ['husband','wife','kid','babies','brother','child','colleague','family']

        words_no_punc = data.translate(str.maketrans('', '', string.punctuation))
        words = data.split()
        agentic = []
        communal = []
        socio_comm = []
        for i in words:
            for j in agentic_terms:
                if j in i.lower():
                    agentic.append(i)
            for j in communal_terms:
                if j in i.lower():
                    communal.append(i)
            for j in socio_communal:
                if j in i.lower():
                    socio_comm.append(i)
        return jsonify({"agentic":agentic, "communal":communal, "socio_communal":socio_comm})
