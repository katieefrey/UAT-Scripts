#! /usr/bin/env python
# -*- coding: utf-8 -*-

#python default packages
import sys
import re
import urllib2
import json


#packages installed on DreamHost
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

# Email libraries
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__, static_folder='static', static_url_path='')


reload(sys)
sys.setdefaultencoding("utf-8")


@app.route('/')
def sortingpage():
    return render_template('sorting.html')

@app.route('/sort/')
def sortingtool():
    return render_template('sorting.html')


@app.route('/topconcepts/')
def send_tc():
    return send_from_directory('topconcepts')


@app.route('/email',methods=['POST'])
def emailchanges():
    val = request.form['testarg']
    msg = MIMEText(val)
    me = '' # TO email address
    you = '' # FROM email address
    msg['Subject'] = 'Suggestions from Sorting Tool'
    msg['From'] = me
    msg['To'] = you


    #Test Info
    #s = smtplib.SMTP('127.0.0.1:1025')
    
    #Live Info
    s = smtplib.SMTP()
    s.connect() # 'mailserver, port'
    s.login()# 'username, password'
    
    #Test & Live
    s.sendmail(me, [you], msg.as_string())
    s.quit()

    #return 'Email sent'

if __name__ == '__main__':
    app.run()

