from flask import Flask, current_app, jsonify
from flask.templating import render_template
import logging
import os
from functools import wraps
import urllib.parse
import string

class anonText():
    def __init__(self):
        self.config = None
    def anonymize(self,text, student_name):
        new_str = text.replace(student_name, "ANON")
        return(new_str)

