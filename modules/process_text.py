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
        word_list = []
        biased_words = []
        for i in words:
            
            association = ""
            flag = False
            for j in male_terms:
                if j in i.lower():
                    #association.append("Male-Gendered")
                    if flag == True:
                        association += ", Male Gendered"
                        flag = True
                    else:
                        association += "Male Gendered"
                        flag = True
            for j in female_terms:
                if j in i.lower():
                    #association.append("Female Gendered")
                    if flag == True:
                        association += ", Female Gendered"
                        flag = True
                    else:
                        association += "Female Gendered"
                        flag = True
            if flag == True:
                biased_words.append(i)
                word_list.append({"word":i, "association":association})
        total_associations = []
        unique_associations = []
        for i in word_list:
            print(i)
            if len(i["association"]) <= 16:
                total_associations.append(i["association"].translate(str.maketrans('', '', string.punctuation)))
        print(total_associations)

        highlighted_text = []
        for i in words:
            if i in biased_words:
                highlighted_text.append(i)
            else:
                highlighted_text.append(i)
        unique_associations = list(set(total_associations))
        return jsonify(word_list), unique_associations, highlighted_text, biased_words
