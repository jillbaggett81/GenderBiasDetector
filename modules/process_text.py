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
        male_terms = ['outstanding','incredible','professional','willing','finest','explanation','direct','normal','horrible','important','sure','courteous','rare','impressed','arrogant','good','easy','kindness','fine','respectful','entire','certain', 'positive','friendly','total','real','great','much','pleased','explain','severe','personal','quick','fantastic','usual','awesome','complete','assertive','confident','aggressive','ambitious','dominan','forceful','independent','daring','outspoken','intellectua','earn','gain','know','insight','think']
        female_terms = ['unprofessional','smart','primary','sweet','poor','new','lowest','unhelpful','happy','hear','difficult','addressed','addressed','convenient','ok','angel','understanding','previous','lovely','sympathetic','kind','help','affection','small','delightful','presbyterian','amazing','understandable','modern','brilliant','spite','several','nasty','multiple','sensitive','nurtur','agreeab','tactful','interpersonal','warm','car','tactful','husband','wife','kid','babies','brother','child','colleague','family']

        words_no_punc = data.translate(str.maketrans('', '', string.punctuation))
        words = words_no_punc.split()
        male = []
        female = []
        for i in words:
            for j in male_terms:
                if j in i.lower():
                    male.append(" "+i)
            for j in female_terms:
                if j in i.lower():
                    female.append(" "+i)
        return jsonify({"male":male, "female":female})
