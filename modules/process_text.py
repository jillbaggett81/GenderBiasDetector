from flask import Flask, current_app, jsonify
from flask.templating import render_template
import logging
import os
from functools import wraps
import urllib.parse
import string
import nltk
import ssl
from nltk.corpus import wordnet


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet')


#Eventually we can epand this class to pull to and from the db as needed.
#This way we can better segment and manipulate our information

#Communal affectionate, helpful, kind, sympathetic,



class ProcessText():
    def __init__(self):
        self.config = None
    def process_text(self,data):
        result = self.process_without_ML(data)
        return(result)
    def findSynonyms(self,word):
        male_terms = ['outstanding','incredible','professional','willing','finest','explanation','direct','normal','horrible','important','sure','courteous','rare','impressed','arrogant','good','easy','kindness','fine','respectful','entire','certain', 'positive','friendly','total','real','great','much','pleased','explain','severe','personal','quick','fantastic','usual','awesome','complete','assertive','confident','aggressive','ambitious','dominan','forceful','independent','daring','outspoken','intellectua','earn','gain','know','insight','think']
        female_terms = ['unprofessional','smart','primary','sweet','poor','new','lowest','unhelpful','happy','hear','difficult','addressed','addressed','convenient','ok','angel','understanding','previous','lovely','sympathetic','kind','help','affection','small','delightful','presbyterian','amazing','understandable','modern','brilliant','spite','several','nasty','multiple','sensitive','nurtur','agreeab','tactful','interpersonal','warm','car','tactful','husband','wife','kid','babies','brother','child','colleague','family']
        synonyms = []
        print("In find synonyms")
        for syn in wordnet.synsets(word):
            for lm in syn.lemmas():
                synonyms.append(lm.name())
        tentative_set = list(set(synonyms))
        print(tentative_set)
        for j in female_terms:
            if j in tentative_set:
                tentative_set.remove(j)
        print(tentative_set)
        return_string = ''
        for k in range(len(tentative_set) -1):
            if '_' in tentative_set[k]:
               tentative_set[k] = tentative_set[k].translate(str.maketrans(' ', ' ', '_'))
            if k < len(tentative_set) -2:
                return_string += tentative_set[k] + ", "
            else:
                return_string += tentative_set[k]
        return return_string
    def process_without_ML(self,data):
        male_terms = ['outstanding','incredible','professional','willing','finest','explanation','direct','normal','horrible','important','sure','courteous','rare','impressed','arrogant','good','easy','kindness','fine','respectful','entire','certain', 'positive','friendly','total','real','great','much','pleased','explain','severe','personal','quick','fantastic','usual','awesome','complete','assertive','confident','aggressive','ambitious','dominan','forceful','independent','daring','outspoken','intellectua','earn','gain','know','insight','think']
        female_terms = ['unprofessional','smart','primary','sweet','poor','new','lowest','unhelpful','happy','hear','difficult','addressed','addressed','convenient','ok','angel','understanding','previous','lovely','sympathetic','kind','help','affection','small','delightful','presbyterian','amazing','understandable','modern','brilliant','spite','several','nasty','multiple','sensitive','nurtur','agreeab','tactful','interpersonal','warm','car','tactful','husband','wife','kid','babies','brother','child','colleague','family']

        words_no_punc = data.translate(str.maketrans('', '', string.punctuation))
        words = words_no_punc.split()
        word_list = []
        biased_words = []
        for i in words:
            self.findSynonyms(i)
            association = ""
            synonym_list = ""
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
                        synonym_list += str(self.findSynonyms(i))
                        association += ", Female Gendered"
                        flag = True
                    else:
                        synonym_list += str(self.findSynonyms(i))
                        association += "Female Gendered"
                        flag = True
            if flag == True:
                biased_words.append(i)
                if synonym_list == "":
                    synonym_list += "No recommended word alternatives found"
                word_list.append({"word":i, "association":association, "synonyms":synonym_list})
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
