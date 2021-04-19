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
        agentic = ['assertive', 'confident', 'aggressive','ambitious', 'dominant', 'forceful', 'independent', 'daring', 'outspoken','intellectual', 'earn', 'gain','do', 'know', 'insight','think']
        communal = ['affectionate', 'helpful', 'kind', 'sympathetic','sensitive', 'nurturing', 'agreeable', 'tactful', 'interpersonal', 'warm', 'caring','tactful']
        sociocomm = ['husband', 'wife', 'kids', 'babies', 'brothers', 'children','colleagues', 'dad', 'family', 'they', 'him', 'her']
        synonyms_1 = {
            'affectionate':['unselfish','devoted','pleasant'],
            'helpful':['cooperative', 'team-oriented','proactive', 'responsible'],
            'kind':['pleasant','good-natured','considerate','attentive','charitable','beneficent'],
            'sympathetic':['understanding','intuitive','encouraging','perceptive'],
            'sensitive':['diplomatic','aware', 'attentive', 'perceptive'],
            'nurturing':['Consider focusing on more professional oriented content'],
            'tactful':['considerate','perceptive'],
            'interpersonal':['civil','team-oriented', 'courteous', 'respectful'],
            'warm':['affable','cordial', 'respectful', 'courteous'],
            'caring':['responsible','concerned','attentive', 'courteous', 'respectful'],
            'agreeable':['amiable','amenable', 'cordial', 'respectful'],
            'lovely' : ['engaging', 'impressive', 'compelling', 'respectful'],
            'insightful' : ['intellectual'],
            'responsive' : ['attentive', 'proactive'],
            'gal':['woman', 'man', 'person', 'candidate'],
            'angel': ['woman', 'man', 'person', 'candidate'],
            'angelic':['engaging', 'impressive', 'compelling', 'respectful'],
            'difficult': [ 'challenging','demanding', 'arduous', 'laborious', 'strenuous', 'burdensome', 'complex', 'involved', 'strong-willed', 'Consider focusing on positive aspects of the candidate. Words beginning with the prefix "un" have been found to raise doubt about the candidate in question. A study by Wayne State University found that “letters for women include doubt raisers at a statistically significant higher rate that is double the rate for males,” (Trix, Psenka). See source.'],
            'unprofessional': ['Consider focusing on positive aspects of the candidate. Words beginning with the prefix "un" have been found to raise doubt about the candidate in question. A study by Wayne State University found that “letters for women include doubt raisers at a statistically significant higher rate that is double the rate for males,” (Trix, Psenka). See source.'],
            'delightful': ['cordial','engaging', 'amenable', 'compelling', 'respectful'],
            'social': ['cordial', 'engaging', 'present', 'compelling', 'respectful'],
            'attractive': ['engaging', 'compelling', 'impressive', 'attentive'],
            'possible': ['feasible', 'viable', 'achievable', 'conceivable'],
            'younger': ['impressive', 'experienced', 'bright', 'sophisticated', 'respectful'],
            'high': ['very', 'strong', 'elevated', 'impressive'],
            'sweet': ['amiable', 'cordial', 'engaging', 'amenable', 'professional', 'respectful'],
            'nasty' : ['Consider focusing on positive aspects of the candidate. A study by Wayne State University found that “letters for women include doubt raisers at a statistically significant higher rate that is double the rate for males,” (Trix, Psenka). See source.'],
            'modern':['knowledgeable', 'contemporary', 'innovative', 'original', 'unique'],
            'tight':['unyielding','compacted','rigid','stiff'],
            'supportive':['encouraging','empowered','team-oriented'],
            'mental':['intellectual','cognitive','conceptual','theoretical'],
            'unprepared':['Consider focusing on positive aspects of the candidate. Words beginning with the prefix "un" have been found to raise doubt about the candidate in question. A study by Wayne State University found that “letters for women include doubt raisers at a statistically significant higher rate that is double the rate for males,” (Trix, Psenka). See source.'],
            'new':['contemporary','innovative', 'beginner','novice'],
            'fellow':['Consider focusing on only the subject of the paper'],
            'unhelpful':['Consider focusing on positive aspects of the candidate. Words beginning with the prefix "un" have been found to raise doubt about the candidate in question. A study by Wayne State University found that “letters for women include doubt raisers at a statistically significant higher rate that is double the rate for males,” (Trix, Psenka). See source.'],
            'poor' : ['Consider focusing on positive aspects of the candidate. A study by Wayne State University found that “letters for women include doubt raisers at a statistically significant higher rate that is double the rate for males,” (Trix, Psenka). See source.'],
            'grateful' : ['appreciative', 'respectful'],
            'honest':['straightforward','clear','genuine', 'respectful'],
            'unclear':['Consider focusing on positive aspects of the candidate. Words beginning with the prefix "un" have been found to raise doubt about the candidate in question. A study by Wayne State University found that “letters for women include doubt raisers at a statistically significant higher rate that is double the rate for males,” (Trix, Psenka). See source.'],
            'presbyterian':['Consider focusing on more professional oriented content.'],
            'extra':['exceptionally','extremely','supplemental','additional'],
            'various':['many','numerous','plethora of', 'myriad']
        }
        female_terms = ['affectionate','helpful','kind','sympathetic','sensitive','nurturing','tactful','interpersonal',
            'warm',
            'caring',
            'agreeable',
            'lovely',
            'insightful',
            'responsive',
            'gal',
            'angel',
            'angelic',
            'difficult',
            'unprofessional',
            'delightful',
            'social',
            'attractive',
            'possible',
            'younger',
            'high',
            'sweet',
            'nasty',
            'modern',
            'tight',
            'supportive',
            'mental',
            'unprepared',
            'new',
            'fellow',
            'unhelpful',
            'poor',
            'grateful',
            'honest',
            'unclear',
            'presbyterian',
            'extra',
            'various']
        return_string = ''
        
        if word in female_terms or word in communal:
            for j in synonyms_1[word]:
                return_string += j + ", "
            #Taking off the last comma
            return_string = return_string[0:-2]
        if return_string == '':
            return_string += "No recommended word alternatives found"
        return return_string
    def process_without_ML(self,data):
        words_to_display = data.split(" ")
        male_terms = ['much','arrogant','kindness','suffered','rudest','outstanding','gentle','certain','finest','willing','stuck','eager','talked','uncomfortable','truthful','busy','easy','confident','tried','independent','positive','lower','assessment','last']
        female_terms = [
            'lovely',
            'insightful',
            'responsive',
            'gal',
            'angel',
            'angelic',
            'difficult',
            'unprofessional',
            'delightful',
            'social',
            'attractive',
            'possible',
            'younger',
            'high',
            'sweet',
            'nasty',
            'modern',
            'tight',
            'supportive',
            'mental',
            'unprepared',
            'new',
            'fellow',
            'unhelpful',
            'poor',
            'grateful',
            'honest',
            'unclear',
            'presbyterian',
            'extra',
            'various']
        agentic = ['assertive', 'confident', 'aggressive','ambitious', 'dominant', 'forceful', 'independent', 'daring', 'outspoken','intellectual', 'earn', 'gain','do', 'know', 'insight','think']
        communal = ['affectionate', 'helpful', 'kind', 'sympathetic','sensitive', 'nurturing', 'agreeable', 'tactful', 'interpersonal', 'warm', 'caring','tactful']
        sociocomm = ['husband', 'wife', 'kids', 'babies', 'brothers', 'children','colleagues', 'dad', 'family']
        synonyms = []
        words_no_punc = data.translate(str.maketrans('', '', string.punctuation))
        words = words_no_punc.split()
        word_list = []
        biased_words = []
        for i in words:
            if i in biased_words:
                continue
            self.findSynonyms(i)
            association = ""
            synonym_list = ""
            flag = False
            for j in male_terms:
                if j == i.lower():
                    #association.append("Male-Gendered")
                    if flag == True:
                        association += ", Professionally Oriented"
                        flag = True
                    else:
                        association += "Professionally Oriented"
                        flag = True
            for j in agentic:
                if j == i.lower():
                    #association.append("Male-Gendered")
                    if flag == True:
                        association += ", Agentic"
                        flag = True
                    else:
                        association += "Agentic"
                        flag = True
            for j in communal:
                if j == i.lower():
                    #association.append("Male-Gendered")
                    if flag == True:
                        synonym_list += str(self.findSynonyms(i))
                        association += ", Communal"
                        flag = True
                    else:
                        synonym_list += str(self.findSynonyms(i))
                        association += "Communal"
                        flag = True
            for j in sociocomm:
                if j == i.lower():
                    #association.append("Male-Gendered")
                    if flag == True:
                        synonym_list += str(self.findSynonyms(i))
                        association += ", Socio-Communal"
                        flag = True
                    else:
                        synonym_list += str(self.findSynonyms(i))
                        association += "Socio-Communal"
                        flag = True
                                   
            for j in female_terms:
                if j == i.lower():
                    #association.append("Female Gendered")
                    if flag == True:
                        synonym_list += str(self.findSynonyms(i))
                        association += ", Potentially Gender Biased"
                        flag = True
                    else:
                        synonym_list += str(self.findSynonyms(i))
                        association += "Potentially Gender Biased"
                        flag = True
            if flag == True:
                biased_words.append(i)
                if synonym_list == "":
                    synonym_list += ""
                word_list.append({"word":i, "association":association, "synonyms":synonym_list})
        total_associations = []
        unique_associations = []
        for i in word_list:
            #if len(i["association"]) <= 16:
            total_associations.append(i["association"].translate(str.maketrans('', '', string.punctuation)))

        highlighted_text = []
        word_bias_display = []
        for i in words_to_display:
            print(i)
            highlighted_text.append(i)
            for j in biased_words:
                if j in i:
                    word_bias_display.append(i)
        unique_associations = list(set(total_associations))


        return jsonify(word_list), unique_associations, highlighted_text, word_bias_display

