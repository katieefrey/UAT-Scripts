#! /usr/bin/env python
# -*- coding: utf-8 -*-

#python default packages
import os
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

import logging
from logging.handlers import RotatingFileHandler

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
    me = os.environ['NOTIFY_FROM'] # FROM email address
    you = os.environ['NOTIFY_TO'] # TO email address
    msg['Subject'] = 'Suggestions from Sorting Tool'
    msg['From'] = me
    msg['To'] = you


    #Test Info
    #s = smtplib.SMTP('127.0.0.1:1025')
    
    #Live Info
    app.logger.info('Connecting to SMTP server %s',os.environ['SMTP_SERVER'])

    s = smtplib.SMTP_SSL()
    s.connect(os.environ['SMTP_SERVER'],465) # 'mailserver, port'
    s.login(os.environ['SMTP_USER'],os.environ['SMTP_PASS'])# 'username, password'

    #Test & Live
    s.sendmail(me, [you], msg.as_string())
    s.quit()

    return 'Email sent'

if __name__ == '__main__':
    # set up logging handler
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=2)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


    # run app
    app.run(host='0.0.0.0')

